from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


FOOTER_BG = "#17324d"
FOOTER_TEXT = "#ffffff"
FOOTER_TEXT_SECONDARY = "#cfd9e3"
FOOTER_HEIGHT = 96
LEFT_X = 70
PRIMARY_Y_OFFSET = 22
SECONDARY_Y_OFFSET = 56
PRIMARY_TEXT = "LAdaxiansheng"
SECONDARY_TEXT = "美股市场简报 · 仅作信息汇总"


def load_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


FONT_PRIMARY = load_font(r"C:\Windows\Fonts\msyhbd.ttc", 22)
FONT_SECONDARY = load_font(r"C:\Windows\Fonts\msyh.ttc", 15)


def update_footer(image_path: Path) -> None:
    with Image.open(image_path).convert("RGB") as img:
        draw = ImageDraw.Draw(img)
        width, height = img.size
        footer_top = height - FOOTER_HEIGHT

        draw.rectangle((0, footer_top, width, height), fill=FOOTER_BG)
        draw.text((LEFT_X, footer_top + PRIMARY_Y_OFFSET), PRIMARY_TEXT, font=FONT_PRIMARY, fill=FOOTER_TEXT)

        secondary_bbox = draw.textbbox((0, 0), SECONDARY_TEXT, font=FONT_SECONDARY)
        secondary_width = secondary_bbox[2] - secondary_bbox[0]
        secondary_x = max(LEFT_X, width - 70 - secondary_width)
        draw.text(
            (secondary_x, footer_top + SECONDARY_Y_OFFSET),
            SECONDARY_TEXT,
            font=FONT_SECONDARY,
            fill=FOOTER_TEXT_SECONDARY,
        )

        temp_path = image_path.with_name(f"{image_path.stem}.footer_tmp{image_path.suffix}")
        img.save(temp_path)

    temp_path.replace(image_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize Dasheng PNG footer branding to LAdaxiansheng.")
    parser.add_argument(
        "--source-dir",
        default=r"C:\Users\mufeng\Documents\大先生财经\美股盘前简报",
        help="Directory that contains the generated PNG brief images.",
    )
    args = parser.parse_args()

    source_dir = Path(args.source_dir)
    image_paths = sorted(source_dir.glob("*.png"))
    if not image_paths:
        raise SystemExit(f"No PNG files found in {source_dir}")

    for image_path in image_paths:
        update_footer(image_path)
        print(image_path)


if __name__ == "__main__":
    main()
