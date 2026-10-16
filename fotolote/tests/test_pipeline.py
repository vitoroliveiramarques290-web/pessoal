import tempfile
import unittest
from pathlib import Path

from PIL import Image

from fotolote import cli
from fotolote.pipeline import run, validate


def make_img(path: Path, size=(400, 200), color=(200, 50, 50)):
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", size, color).save(path)


class PipelineTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.inp, self.out = self.tmp / "in", self.tmp / "out"
        make_img(self.inp / "a.jpg")
        make_img(self.inp / "sub" / "b.png", (100, 300))
        (self.inp / "nota.txt").write_text("x")

    def test_resize_max_side_keeps_ratio_and_never_upscales(self):
        run(self.inp, self.out, {"operations": [{"op": "resize", "max_side": 100}]})
        self.assertEqual(Image.open(self.out / "a.jpg").size, (100, 50))
        make_img(self.inp / "small.jpg", (50, 30))
        run(self.inp / "small.jpg", self.out, {"operations": [{"op": "resize", "max_side": 100}]})
        self.assertEqual(Image.open(self.out / "small.jpg").size, (50, 30))

    def test_recursive_preserves_structure_and_converts_format(self):
        res = run(self.inp, self.out, {"output": {"format": "webp", "suffix": "_x"}}, recursive=True, workers=1)
        self.assertEqual(sum(r.status == "ok" for r in res), 2)
        self.assertTrue((self.out / "sub" / "b_x.webp").exists())

    def test_crop_ratio_and_cover(self):
        cfg = {"operations": [{"op": "crop_ratio", "ratio": "1:1"}, {"op": "resize", "width": 64, "height": 64, "fit": "cover"}]}
        run(self.inp / "a.jpg", self.out, cfg)
        self.assertEqual(Image.open(self.out / "a.jpg").size, (64, 64))

    def test_rename_pattern(self):
        run(self.inp, self.out, {"output": {"rename": "foto_{n:03d}"}}, workers=1)
        self.assertTrue((self.out / "foto_001.jpg").exists())

    def test_skip_existing_unless_overwrite(self):
        run(self.inp / "a.jpg", self.out, {})
        r = run(self.inp / "a.jpg", self.out, {})[0]
        self.assertEqual(r.status, "skipped")
        self.assertEqual(run(self.inp / "a.jpg", self.out, {}, overwrite=True)[0].status, "ok")

    def test_bad_file_does_not_stop_batch(self):
        (self.inp / "quebrada.jpg").write_bytes(b"nao sou imagem")
        res = run(self.inp, self.out, {}, workers=1)
        self.assertEqual(sorted(r.status for r in res), ["error", "ok"])

    def test_all_ops_run(self):
        ops = [{"op": o} for o in ("autocontrast", "grayscale", "sepia")] + [
            {"op": "brightness", "factor": 1.2}, {"op": "contrast", "factor": 1.1},
            {"op": "saturation", "factor": 0.8}, {"op": "sharpness", "factor": 1.5},
            {"op": "blur", "radius": 1}, {"op": "rotate", "degrees": 90},
            {"op": "flip"}, {"op": "border", "size": 4},
            {"op": "watermark", "text": "teste", "position": "center"}]
        r = run(self.inp / "a.jpg", self.out, {"operations": ops})[0]
        self.assertEqual(r.status, "ok", r.detail)

    def test_png_with_alpha_to_jpg(self):
        Image.new("RGBA", (20, 20), (1, 2, 3, 0)).save(self.inp / "t.png")
        r = run(self.inp / "t.png", self.out, {"output": {"format": "jpg"}})[0]
        self.assertEqual(r.status, "ok", r.detail)

    def test_validate_rejects_unknown(self):
        with self.assertRaises(ValueError):
            validate({"operations": [{"op": "inexistente"}]})

    def test_cli_and_dry_run(self):
        self.assertEqual(cli.main([str(self.inp), "-o", str(self.out), "--max-lado", "50", "--pb", "--dry-run"]), 0)
        self.assertFalse(self.out.exists())
        self.assertEqual(cli.main([str(self.inp), "-o", str(self.out), "--max-lado", "50", "--pb"]), 0)
        self.assertEqual(cli.main([str(self.inp), "-o", str(self.inp)]), 2)


if __name__ == "__main__":
    unittest.main()
