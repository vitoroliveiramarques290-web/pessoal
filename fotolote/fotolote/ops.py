"""Operações de imagem. Cada operação recebe (img, **params) e devolve uma imagem."""
from __future__ import annotations

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps


def resize(img, width=None, height=None, max_side=None, fit="contain", upscale=False):
    """fit: contain (cabe dentro), cover (preenche e corta), exact (distorce)."""
    w, h = img.size
    if max_side:
        scale = max_side / max(w, h)
        if scale >= 1 and not upscale:
            return img
        return img.resize((max(1, round(w * scale)), max(1, round(h * scale))), Image.LANCZOS)
    if not width and not height:
        return img
    width = width or round(w * height / h)
    height = height or round(h * width / w)
    if fit == "exact":
        return img.resize((width, height), Image.LANCZOS)
    if fit == "cover":
        return ImageOps.fit(img, (width, height), Image.LANCZOS)
    scale = min(width / w, height / h)
    if scale >= 1 and not upscale:
        return img
    return img.resize((max(1, round(w * scale)), max(1, round(h * scale))), Image.LANCZOS)


def crop_ratio(img, ratio="1:1"):
    """Corte central na proporção dada, ex.: '1:1', '16:9', '4:5'."""
    rw, rh = (float(x) for x in str(ratio).split(":"))
    target = rw / rh
    w, h = img.size
    if w / h > target:
        nw, nh = round(h * target), h
    else:
        nw, nh = w, round(w / target)
    left, top = (w - nw) // 2, (h - nh) // 2
    return img.crop((left, top, left + nw, top + nh))


def rotate(img, degrees=0):
    return img.rotate(-degrees, expand=True, resample=Image.BICUBIC) if degrees else img


def flip(img, direction="horizontal"):
    return ImageOps.mirror(img) if direction == "horizontal" else ImageOps.flip(img)


def _enhance(cls, img, factor):
    return cls(img).enhance(factor)


def brightness(img, factor=1.0):
    return _enhance(ImageEnhance.Brightness, img, factor)


def contrast(img, factor=1.0):
    return _enhance(ImageEnhance.Contrast, img, factor)


def saturation(img, factor=1.0):
    return _enhance(ImageEnhance.Color, img, factor)


def sharpness(img, factor=1.0):
    return _enhance(ImageEnhance.Sharpness, img, factor)


def autocontrast(img, cutoff=1):
    return ImageOps.autocontrast(img.convert("RGB"), cutoff=cutoff)


def grayscale(img):
    return ImageOps.grayscale(img).convert("RGB")


def sepia(img):
    gray = ImageOps.grayscale(img)
    return ImageOps.colorize(gray, black="#2b1a0a", white="#f4e4c1", mid="#a67c52")


def blur(img, radius=2):
    return img.filter(ImageFilter.GaussianBlur(radius))


def border(img, size=10, color="white"):
    return ImageOps.expand(img.convert("RGB"), border=size, fill=color)


def _font(size):
    for name in ("DejaVuSans.ttf", "Arial.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default(size)


def watermark(img, text="", position="bottom-right", opacity=0.6, size_pct=4, color="white", margin_pct=2):
    """Marca d'água de texto; o tamanho da fonte é % da largura da imagem."""
    if not text:
        return img
    base = img.convert("RGBA")
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    font = _font(max(10, round(base.width * size_pct / 100)))
    l, t, r, b = draw.textbbox((0, 0), text, font=font)
    tw, th = r - l, b - t
    m = round(base.width * margin_pct / 100)
    vert, _, horiz = position.partition("-")
    x = {"left": m, "right": base.width - tw - m, "center": (base.width - tw) // 2}.get(horiz or "center", m)
    y = {"top": m, "bottom": base.height - th - m, "center": (base.height - th) // 2}.get(vert, m)
    rgb = ImageDraw.ImageColor.getrgb(color)
    draw.text((x - l, y - t), text, font=font, fill=(*rgb[:3], round(255 * opacity)))
    return Image.alpha_composite(base, layer).convert("RGB")


OPS = {
    "resize": resize, "crop_ratio": crop_ratio, "rotate": rotate, "flip": flip,
    "brightness": brightness, "contrast": contrast, "saturation": saturation,
    "sharpness": sharpness, "autocontrast": autocontrast, "grayscale": grayscale,
    "sepia": sepia, "blur": blur, "border": border, "watermark": watermark,
}
