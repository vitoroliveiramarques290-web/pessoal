"""Descoberta de arquivos, execução do pipeline e processamento paralelo."""
from __future__ import annotations

import json
import os
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageOps

from .ops import OPS

INPUT_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff", ".gif"}
FORMATS = {"jpg": ("JPEG", ".jpg"), "jpeg": ("JPEG", ".jpg"), "png": ("PNG", ".png"),
           "webp": ("WEBP", ".webp"), "tiff": ("TIFF", ".tif")}


@dataclass
class Result:
    src: str
    dst: str | None
    status: str  # ok | skipped | error
    detail: str = ""


def load_config(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def validate(config: dict) -> None:
    for step in config.get("operations", []):
        if step.get("op") not in OPS:
            raise ValueError(f"operação desconhecida: {step.get('op')!r} (disponíveis: {', '.join(OPS)})")
    fmt = config.get("output", {}).get("format")
    if fmt and fmt.lower() not in FORMATS:
        raise ValueError(f"formato desconhecido: {fmt!r} (disponíveis: {', '.join(FORMATS)})")


def find_images(inp: Path, recursive: bool) -> list[Path]:
    if inp.is_file():
        return [inp]
    it = inp.rglob("*") if recursive else inp.glob("*")
    return sorted(p for p in it if p.is_file() and p.suffix.lower() in INPUT_EXTS)


def output_path(src: Path, root: Path, out_dir: Path, out_cfg: dict, index: int) -> Path:
    fmt = out_cfg.get("format")
    ext = FORMATS[fmt.lower()][1] if fmt else (".jpg" if src.suffix.lower() == ".jpeg" else src.suffix.lower())
    rel_dir = src.parent.relative_to(root) if root.is_dir() else Path()
    pattern = out_cfg.get("rename")
    stem = pattern.format(n=index, name=src.stem) if pattern else src.stem + out_cfg.get("suffix", "")
    return out_dir / rel_dir / (stem + ext)


def process_one(args) -> Result:
    src, dst, config, overwrite = args
    src, dst = Path(src), Path(dst)
    try:
        if dst.exists() and not overwrite:
            return Result(str(src), str(dst), "skipped", "já existe (use --overwrite)")
        out_cfg = config.get("output", {})
        with Image.open(src) as im:
            img = ImageOps.exif_transpose(im)
            exif = None if out_cfg.get("strip_exif", True) else im.info.get("exif")
            img = img.convert("RGBA") if img.mode in ("P", "LA") else img
            for step in config.get("operations", []):
                params = {k: v for k, v in step.items() if k != "op"}
                img = OPS[step["op"]](img, **params)
        fmt_name = FORMATS[out_cfg["format"].lower()][0] if out_cfg.get("format") else (img.format or "JPEG")
        if fmt_name == "JPEG" and img.mode != "RGB":
            img = img.convert("RGB")
        save = {}
        if fmt_name in ("JPEG", "WEBP"):
            save["quality"] = out_cfg.get("quality", 85)
        if fmt_name == "JPEG":
            save.update(optimize=True, progressive=True)
        if exif and fmt_name in ("JPEG", "WEBP", "PNG"):
            save["exif"] = exif
        dst.parent.mkdir(parents=True, exist_ok=True)
        img.save(dst, fmt_name, **save)
        return Result(str(src), str(dst), "ok", f"{src.stat().st_size // 1024} KB -> {dst.stat().st_size // 1024} KB")
    except Exception as e:  # uma foto ruim não pode derrubar o lote
        return Result(str(src), str(dst), "error", f"{type(e).__name__}: {e}")


def run(inp: Path, out_dir: Path, config: dict, recursive=False, overwrite=False,
        workers: int | None = None, dry_run=False, on_result=None) -> list[Result]:
    validate(config)
    files = find_images(inp, recursive)
    out_cfg = config.get("output", {})
    jobs = [(str(f), str(output_path(f, inp, out_dir, out_cfg, i)), config, overwrite)
            for i, f in enumerate(files, 1)]
    if dry_run:
        results = [Result(s, d, "skipped", "dry-run") for s, d, *_ in jobs]
    elif len(jobs) <= 1 or workers == 1:
        results = [process_one(j) for j in jobs]
    else:
        with ProcessPoolExecutor(max_workers=workers or os.cpu_count()) as ex:
            results = list(ex.map(process_one, jobs, chunksize=4))
    for r in results:
        if on_result:
            on_result(r)
    return results
