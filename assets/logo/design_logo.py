#!/usr/bin/env python
"""Generate the Jaon logo in modern geometric style."""
import io
import math
import struct
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


# Modern tech palette
COLORS = {
    "deep_space": "#0B0F19",
    "indigo": "#1E1B4B",
    "violet": "#6366F1",
    "cyan": "#06B6D4",
    "gold": "#F59E0B",
    "white": "#F8FAFC",
    "muted": "#94A3B8",
}


def hex_to_rgba(hex_color: str, alpha: int = 255) -> tuple:
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4)) + (alpha,)


def blend_rgba(c1, c2, ratio):
    return tuple(int(c1[i] * (1 - ratio) + c2[i] * ratio) for i in range(4))


def blend_rgb(c1, c2, ratio):
    return tuple(int(c1[i] * (1 - ratio) + c2[i] * ratio) for i in range(3))


def radial_gradient(draw, center, radius, inner, outer):
    """Draw a smooth radial gradient disk."""
    cx, cy = center
    for r in range(radius, 0, -1):
        ratio = (r / radius) ** 0.9
        color = blend_rgba(inner, outer, ratio)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)


def draw_nested_squares(draw, center, radius, color):
    """Draw a minimal mark of three nested rounded squares + a dot."""
    cx, cy = center

    # Outer rounded square outline
    outer = radius * 0.80
    draw.rounded_rectangle(
        [cx - outer, cy - outer, cx + outer, cy + outer],
        radius=outer * 0.30,
        outline=color,
        width=max(2, int(radius * 0.08)),
    )

    # Middle rounded square outline
    middle = radius * 0.52
    draw.rounded_rectangle(
        [cx - middle, cy - middle, cx + middle, cy + middle],
        radius=middle * 0.30,
        outline=color,
        width=max(2, int(radius * 0.07)),
    )

    # Inner solid rounded square
    inner = radius * 0.28
    draw.rounded_rectangle(
        [cx - inner, cy - inner, cx + inner, cy + inner],
        radius=inner * 0.30,
        fill=color,
    )

    # Central dot
    dot_r = radius * 0.10
    draw.ellipse(
        [cx - dot_r, cy - dot_r, cx + dot_r, cy + dot_r],
        fill=hex_to_rgba(COLORS["indigo"]),
    )


def create_logo(size: int) -> Image.Image:
    """Create the modern Jaon logo."""
    scale = 4
    big = size * scale
    img = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx = cy = big // 2

    # Main disk
    disk_r = int(big * 0.34)
    radial_gradient(
        draw,
        (cx, cy),
        disk_r,
        hex_to_rgba(COLORS["indigo"]),
        blend_rgba(hex_to_rgba(COLORS["violet"]), (0, 0, 0, 255), 0.55),
    )

    # Inner glow
    glow_r = int(big * 0.18)
    radial_gradient(
        draw,
        (cx, cy),
        glow_r,
        hex_to_rgba(COLORS["violet"], 140),
        hex_to_rgba(COLORS["indigo"], 0),
    )

    # Nested squares mark
    mark_r = int(big * 0.14)
    draw_nested_squares(draw, (cx, cy), mark_r, hex_to_rgba(COLORS["white"], 245))

    # Downscale
    if size != big:
        img = img.resize((size, size), Image.Resampling.LANCZOS)

    return img


def _load_fonts(height: int):
    """Load banner/social fonts, falling back to default."""
    candidates_large = ["arialbd.ttf", "Arial Bold.ttf", "DejaVuSans-Bold.ttf"]
    candidates_small = ["arial.ttf", "Arial.ttf", "DejaVuSans.ttf"]

    font_large = None
    for name in candidates_large:
        try:
            font_large = ImageFont.truetype(name, int(height * 0.34))
            break
        except OSError:
            continue

    font_small = None
    for name in candidates_small:
        try:
            font_small = ImageFont.truetype(name, int(height * 0.12))
            break
        except OSError:
            continue

    return font_large or ImageFont.load_default(), font_small or ImageFont.load_default()


def create_banner(width: int, height: int) -> Image.Image:
    """Create a horizontal banner with the logo and text."""
    bg = hex_to_rgba(COLORS["deep_space"])
    text = hex_to_rgba(COLORS["white"])
    muted = hex_to_rgba(COLORS["muted"])

    img = Image.new("RGBA", (width, height), bg)
    draw = ImageDraw.Draw(img)

    logo_size = int(height * 0.58)
    logo = create_logo(logo_size)
    img.paste(logo, (int(height * 0.14), int((height - logo_size) / 2)), logo)

    font_large, font_small = _load_fonts(height)

    text_x = int(height * 0.14) + logo_size + int(height * 0.12)
    bbox = draw.textbbox((0, 0), "Jaon", font=font_large)
    draw.text(
        (text_x, (height - (bbox[3] - bbox[1])) // 2 - bbox[1] - int(height * 0.04)),
        "Jaon",
        fill=text,
        font=font_large,
    )

    tagline = "Python simplicity, Java rigor"
    tb = draw.textbbox((0, 0), tagline, font=font_small)
    draw.text(
        (text_x, (height + (bbox[3] - bbox[1])) // 2 - tb[1] + int(height * 0.02)),
        tagline,
        fill=muted,
        font=font_small,
    )

    return img


def create_social(width: int, height: int) -> Image.Image:
    """Create a social media preview image with centered logo and text."""
    bg = hex_to_rgba(COLORS["deep_space"])
    text_color = hex_to_rgba(COLORS["white"])
    muted = hex_to_rgba(COLORS["muted"])

    img = Image.new("RGBA", (width, height), bg)
    draw = ImageDraw.Draw(img)

    logo_size = int(height * 0.42)
    logo = create_logo(logo_size)
    img.paste(logo, ((width - logo_size) // 2, int(height * 0.14)), logo)

    try:
        font_large = ImageFont.truetype("arialbd.ttf", int(height * 0.17))
        font_small = ImageFont.truetype("arial.ttf", int(height * 0.06))
    except OSError:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), "Jaon", font=font_large)
    text_width = bbox[2] - bbox[0]
    draw.text(
        ((width - text_width) // 2 - bbox[0], int(height * 0.62)),
        "Jaon",
        fill=text_color,
        font=font_large,
    )

    tagline = "A programming language blending Python simplicity with Java rigor"
    tb = draw.textbbox((0, 0), tagline, font=font_small)
    tagline_width = tb[2] - tb[0]
    draw.text(
        ((width - tagline_width) // 2 - tb[0], int(height * 0.80)),
        tagline,
        fill=muted,
        font=font_small,
    )

    return img


def save_ico(images: list[Image.Image], path: Path) -> None:
    """Save multiple images as a multi-size Windows ICO file."""
    png_buffers = []
    for img in images:
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        png_buffers.append(buf.getvalue())

    count = len(images)
    header = struct.pack("<HHH", 0, 1, count)

    entries = b""
    data_offset = 6 + 16 * count
    data = b""

    for img, png_bytes in zip(images, png_buffers):
        w, h = img.size
        width_byte = w if w < 256 else 0
        height_byte = h if h < 256 else 0
        size = len(png_bytes)
        entries += struct.pack(
            "<BBBBHHII",
            width_byte,
            height_byte,
            0,  # colors
            0,  # reserved
            1,  # color planes
            32,  # bits per pixel
            size,
            data_offset,
        )
        data += png_bytes
        data_offset += size

    with open(path, "wb") as f:
        f.write(header + entries + data)


def main():
    out_dir = Path(__file__).resolve().parent
    out_dir.mkdir(parents=True, exist_ok=True)

    sizes = [16, 32, 48, 64, 128, 256, 512, 1024]
    images = {}

    for size in sizes:
        logo = create_logo(size)
        logo.save(out_dir / f"jaon-logo-{size}x{size}.png")
        images[size] = logo
        print(f"Saved jaon-logo-{size}x{size}.png")

    ico_sizes = [16, 32, 48, 64, 128, 256]
    ico_images = [images[s] for s in ico_sizes]
    save_ico(ico_images, out_dir / "jaon-logo.ico")
    print("Saved jaon-logo.ico")

    banner = create_banner(1200, 400)
    banner.save(out_dir / "jaon-banner.png")
    print("Saved jaon-banner.png")

    social = create_social(1280, 640)
    social.save(out_dir / "jaon-social.png")
    print("Saved jaon-social.png")


if __name__ == "__main__":
    main()
