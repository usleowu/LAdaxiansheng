from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def sync_assets(source_dir: Path, target_dir: Path) -> None:
    source_dir = source_dir.resolve()
    target_dir = target_dir.resolve()
    target_dir.mkdir(parents=True, exist_ok=True)

    source_files = {path.name: path for path in source_dir.glob("*.png")}
    target_files = {path.name: path for path in target_dir.glob("*.png")}

    for name, source_path in source_files.items():
        shutil.copy2(source_path, target_dir / name)

    for name, target_path in target_files.items():
        if name not in source_files:
            target_path.unlink()


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync Dasheng brief PNG assets into the repo for GitHub Pages.")
    parser.add_argument(
        "--source-dir",
        default=r"C:\Users\mufeng\Documents\大先生财经\美股盘前简报",
        help="Local directory that contains the generated PNG files.",
    )
    parser.add_argument(
        "--target-dir",
        default=r"C:\Users\mufeng\Documents\Codex\2026-06-05\analyze-a-public-company-pull-the\dasheng_brief_assets",
        help="Repo directory where PNG files will be copied for GitHub Pages builds.",
    )
    args = parser.parse_args()
    sync_assets(Path(args.source_dir), Path(args.target_dir))


if __name__ == "__main__":
    main()
