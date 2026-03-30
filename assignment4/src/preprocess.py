from __future__ import annotations

import argparse

from config_loader import load_config
from utils.io_paths import get_project_root


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Preprocess thesis data.")
    parser.add_argument("--config", required=True, help="Path to YAML configuration file.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    root = get_project_root()

    raw_dir = root / config["paths"]["raw_data_dir"]
    processed_dir = root / config["paths"]["processed_data_dir"]
    processed_dir.mkdir(parents=True, exist_ok=True)

    placeholder_output = processed_dir / "README_preprocessing_output.txt"
    placeholder_output.write_text(
        "This placeholder confirms where a processed analytical dataset would be saved.\n"
        f"Raw data directory: {raw_dir}\n"
        "The real implementation should merge GP list sizes, demographics, workforce, and hospital use data.\n",
        encoding="utf-8",
    )

    print(f"Preprocessing scaffold executed successfully. Output directory: {processed_dir}")


if __name__ == "__main__":
    main()
