from __future__ import annotations

import argparse

from config_loader import load_config
from utils.io_paths import get_project_root


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect experiment outputs.")
    parser.add_argument("--config", required=True, help="Path to YAML configuration file.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    root = get_project_root()

    report_path = root / config["paths"]["reports_dir"] / f"{config['experiment']['name']}_run.json"
    if report_path.exists():
        print(report_path.read_text(encoding="utf-8"))
    else:
        print("No report found yet for this experiment. Run training first to generate traceable output metadata.")


if __name__ == "__main__":
    main()
