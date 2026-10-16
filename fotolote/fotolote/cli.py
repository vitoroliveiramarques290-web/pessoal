"""Interface de linha de comando: python -m fotolote ENTRADA -o SAIDA [opções]."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .pipeline import FORMATS, load_config, run


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="fotolote", description="Edição de fotos em lote.")
    p.add_argument("entrada", help="pasta ou arquivo de imagem")
    p.add_argument("-o", "--saida", required=True, help="pasta de saída (a original nunca é alterada)")
    p.add_argument("-p", "--preset", help="arquivo JSON com operações e saída")
    p.add_argument("-r", "--recursivo", action="store_true", help="incluir subpastas")
    p.add_argument("--overwrite", action="store_true", help="sobrescrever arquivos existentes")
    p.add_argument("--dry-run", action="store_true", help="só listar o que seria feito")
    p.add_argument("-j", "--workers", type=int, help="processos paralelos (padrão: nº de CPUs)")
    p.add_argument("--version", action="version", version=__version__)

    g = p.add_argument_group("operações rápidas (aplicadas depois do preset, nesta ordem)")
    g.add_argument("--max-lado", type=int, metavar="PX", help="maior lado máximo, mantém proporção")
    g.add_argument("--largura", type=int)
    g.add_argument("--altura", type=int)
    g.add_argument("--fit", choices=["contain", "cover", "exact"], default="contain")
    g.add_argument("--corte", metavar="W:H", help="corte central na proporção, ex.: 1:1, 16:9")
    g.add_argument("--girar", type=float, metavar="GRAUS", help="horário")
    g.add_argument("--brilho", type=float, metavar="F", help="1.0 = original")
    g.add_argument("--contraste", type=float, metavar="F")
    g.add_argument("--saturacao", type=float, metavar="F")
    g.add_argument("--nitidez", type=float, metavar="F")
    g.add_argument("--auto-contraste", action="store_true")
    g.add_argument("--pb", action="store_true", help="preto e branco")
    g.add_argument("--sepia", action="store_true")
    g.add_argument("--marca", metavar="TEXTO", help="marca d'água de texto")
    g.add_argument("--marca-pos", default="bottom-right", help="ex.: top-left, bottom-right, center")

    o = p.add_argument_group("saída")
    o.add_argument("--formato", choices=sorted(FORMATS))
    o.add_argument("--qualidade", type=int, help="1-100 (JPEG/WEBP)")
    o.add_argument("--sufixo", help="sufixo no nome, ex.: _web")
    o.add_argument("--renomear", metavar="PADRAO", help="ex.: 'viagem_{n:03d}' ({n}=sequência, {name}=nome original)")
    o.add_argument("--manter-exif", action="store_true", help="por padrão o EXIF (inclui GPS) é removido")
    return p


def config_from_args(a: argparse.Namespace) -> dict:
    cfg = load_config(a.preset) if a.preset else {}
    ops = list(cfg.get("operations", []))
    if a.max_lado or a.largura or a.altura:
        ops.append({"op": "resize", "max_side": a.max_lado, "width": a.largura, "height": a.altura, "fit": a.fit})
    if a.corte:
        ops.append({"op": "crop_ratio", "ratio": a.corte})
    if a.girar:
        ops.append({"op": "rotate", "degrees": a.girar})
    if a.auto_contraste:
        ops.append({"op": "autocontrast"})
    for flag, name in ((a.brilho, "brightness"), (a.contraste, "contrast"),
                       (a.saturacao, "saturation"), (a.nitidez, "sharpness")):
        if flag is not None:
            ops.append({"op": name, "factor": flag})
    if a.pb:
        ops.append({"op": "grayscale"})
    if a.sepia:
        ops.append({"op": "sepia"})
    if a.marca:
        ops.append({"op": "watermark", "text": a.marca, "position": a.marca_pos})
    out = dict(cfg.get("output", {}))
    for key, val in (("format", a.formato), ("quality", a.qualidade), ("suffix", a.sufixo), ("rename", a.renomear)):
        if val is not None:
            out[key] = val
    if a.manter_exif:
        out["strip_exif"] = False
    return {"operations": ops, "output": out}


def main(argv=None) -> int:
    a = build_parser().parse_args(argv)
    inp, out = Path(a.entrada), Path(a.saida)
    if not inp.exists():
        print(f"erro: {inp} não existe", file=sys.stderr)
        return 2
    if inp.is_dir() and out.resolve() == inp.resolve():
        print("erro: a saída deve ser diferente da entrada", file=sys.stderr)
        return 2
    try:
        cfg = config_from_args(a)
        icon = {"ok": "✓", "skipped": "-", "error": "✗"}
        results = run(inp, out, cfg, a.recursivo, a.overwrite, a.workers, a.dry_run,
                      on_result=lambda r: print(f"{icon[r.status]} {r.src} -> {r.dst}  {r.detail}"))
    except (ValueError, OSError) as e:
        print(f"erro: {e}", file=sys.stderr)
        return 2
    n = {s: sum(r.status == s for r in results) for s in ("ok", "skipped", "error")}
    print(f"\n{len(results)} arquivo(s): {n['ok']} ok, {n['skipped']} ignorado(s), {n['error']} erro(s)")
    return 1 if n["error"] else 0


if __name__ == "__main__":
    sys.exit(main())
