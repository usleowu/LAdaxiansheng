from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


DEFAULT_RENDERER = Path(r"C:\Users\mufeng\Documents\Codex\2026-06-23\new-chat\generate_dasheng_summary.py")
DEFAULT_OUTPUT_DIR = Path(r"C:\Users\mufeng\Documents\大先生财经\美股盘前简报")


def run_renderer(renderer: Path, input_json: Path, output_png: Path, layout: str) -> None:
    cmd = [sys.executable, str(renderer), str(input_json), str(output_png)]
    if layout != "portrait":
        cmd.extend(["--layout", layout])
    subprocess.run(cmd, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Render both portrait and 1:1 Dasheng daily brief PNGs.")
    parser.add_argument("input_json", help="Path to the JSON payload.")
    parser.add_argument(
        "--basename",
        required=True,
        help="Base output filename without .png, for example 2026-08-02-美股盘前信息简报",
    )
    parser.add_argument(
        "--renderer",
        default=str(DEFAULT_RENDERER),
        help="Renderer script path.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory where the PNG files will be written.",
    )
    args = parser.parse_args()

    input_json = Path(args.input_json).resolve()
    renderer = Path(args.renderer).resolve()
    output_dir = Path(args.output_dir).resolve()
    portrait_path = output_dir / f"{args.basename}.png"
    square_path = output_dir / f"{args.basename}-1x1.png"

    run_renderer(renderer, input_json, portrait_path, "portrait")
    run_renderer(renderer, input_json, square_path, "square")

    print(portrait_path)
    print(square_path)


if __name__ == "__main__":
    main()
