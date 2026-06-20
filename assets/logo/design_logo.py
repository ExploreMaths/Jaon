#!/usr/bin/env python
"""Generate the Helios logo in modern geometric style."""
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


def draw_ring_segment(draw, center, radius, width, start_angle, end_angle, color):
    """Draw an annular arc segment."""
    cx, cy = center
    bbox = [cx - radius, cy - radius, cx + radius, cy + radius]
    draw.arc(bbox, start=start_angle, end=end_angle, fill=color, width=width)


def draw_glow(draw, center, radius, color, steps=40):
    """Draw a soft glow behind a point."""
    cx, cy = center
    base = hex_to_rgba(color)
    for i in range(steps, 0, -1):
        ratio = i / steps
        alpha = int(80 * ratio ** 2)
        r = radius * (1 + 0.6 * (1 - ratio))
        draw.ellipse(
            [cx - r, cy - r, cx + r, cy + r],
            fill=base[:3] + (alpha,),
        )


def draw_modern_h(draw, center, radius, color):
    """Draw a geometric, slightly tech-styled H mark."""
    cx, cy = center
    bar = radius * 0.22
    half_h = radius * 0.62
    half_w = radius * 0.42
    radius_corner = bar * 0.5

    # Left vertical bar
    draw.rounded_rectangle(
        [cx - half_w - bar / 2, cy - half_h, cx - half_w + bar / 2, cy + half_h],
        radius=radius_corner,
        fill=color,
    )
    # Right vertical bar
    draw.rounded_rectangle(
        [cx + half_w - bar / 2, cy - half_h, cx + half_w + bar / 2, cy + half_h],
        radius=radius_corner,
        fill=color,
    )
    # Horizontal connector, slightly thinner
    h_bar = bar * 0.75
    draw.rounded_rectangle(
        [cx - half_w + bar / 2, cy - h_bar / 2, cx + half_w - bar / 2, cy + h_bar / 2],
        radius=h_bar * 0.5,
        fill=color,
    )


def create_logo(size: int) -> Image.Image:
    """Create the modern Helios logo."""
    scale = 4
    big = size * scale
    img = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx = cy = big // 2

    # Proportions relative to canvas
    orbit_radius = int(big * 0.40)
    orbit_width = max(2, int(big * 0.025))
    disk_radius = int(big * 0.28)
    core_radius = int(big * 0.18)
    sun_radius = int(big * 0.07)

    # Orbit gap angle: the sun sits at the gap
    gap_deg = 42
    start_orbit = 25
    end_orbit = 360 - gap_deg

    # Soft orbit glow
    glow_radius = orbit_radius + orbit_width * 3
    draw_glow(draw, (cx, cy), glow_radius, COLORS["violet"], steps=60)

    # Orbit ring gradient: draw many thin arcs
    for i in range(orbit_width):
        ratio = i / (orbit_width - 1) if orbit_width > 1 else 0
        # Outer edge cyan, inner edge violet
        color = blend_rgba(hex_to_rgba(COLORS["cyan"]), hex_to_rgba(COLORS["violet"]), ratio)
        r = orbit_radius - orbit_width // 2 + i
        draw.arc(
            [cx - r, cy - r, cx + r, cy + r],
            start=start_orbit,
            end=end_orbit,
            fill=color,
            width=1,
        )

    # Main disk
    radial_gradient(
        draw,
        (cx, cy),
        disk_radius,
        hex_to_rgba(COLORS["indigo"]),
        blend_rgba(hex_to_rgba(COLORS["violet"]), (0, 0, 0, 255), 0.55),
    )

    # Inner core glow
    radial_gradient(
        draw,
        (cx, cy),
        core_radius,
        hex_to_rgba(COLORS["violet"], 160),
        hex_to_rgba(COLORS["indigo"], 0),
    )

    # Subtle edge ring
    edge_ring = int(disk_radius * 0.92)
    draw.ellipse(
        [cx - edge_ring, cy - edge_ring, cx + edge_ring, cy + edge_ring],
        outline=hex_to_rgba(COLORS["cyan"], 80),
        width=max(1, big // 200),
    )

    # Sun orb at the orbit gap
    sun_angle = math.radians(-gap_deg / 2)
    sx = cx + orbit_radius * math.cos(sun_angle)
    sy = cy + orbit_radius * math.sin(sun_angle)

    draw_glow(draw, (sx, sy), sun_radius * 1.6, COLORS["gold"], steps=30)
    radial_gradient(
        draw,
        (sx, sy),
        sun_radius,
        (255, 255, 255, 240),
        hex_to_rgba(COLORS["gold"]),
    )

    # Modern H mark
    h_radius = int(big * 0.14)
    draw_modern_h(draw, (cx, cy), h_radius, hex_to_rgba(COLORS["white"], 245))

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
    bbox = draw.textbbox((0, 0), "Helios", font=font_large)
    draw.text(
        (text_x, (height - (bbox[3] - bbox[1])) // 2 - bbox[1] - int(height * 0.04)),
        "Helios",
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

    bbox = draw.textbbox((0, 0), "Helios", font=font_large)
    text_width = bbox[2] - bbox[0]
    draw.text(
        ((width - text_width) // 2 - bbox[0], int(height * 0.62)),
        "Helios",
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
        logo.save(out_dir / f"helios-logo-{size}x{size}.png")
        images[size] = logo
        print(f"Saved helios-logo-{size}x{size}.png")

    ico_sizes = [16, 32, 48, 64, 128, 256]
    ico_images = [images[s] for s in ico_sizes]
    save_ico(ico_images, out_dir / "helios-logo.ico")
    print("Saved helios-logo.ico")

    banner = create_banner(1200, 400)
    banner.save(out_dir / "helios-banner.png")
    print("Saved helios-banner.png")

    social = create_social(1280, 640)
    social.save(out_dir / "helios-social.png")
    print("Saved helios-social.png")


if __name__ == "__main__":
    main()
