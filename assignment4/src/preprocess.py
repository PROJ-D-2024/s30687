from __future__ import annotations

import argparse
from pathlib import Path

from src.config_loader import load_config
from src.data_pipeline import build_analytical_dataset, save_processed_outputs
from src.utils.io_paths import get_project_root


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Preprocess thesis data.")
    parser.add_argument("--config", required=True, help="Path to YAML configuration file.")
    return parser.parse_args()


def run_preprocessing(config_path: str | Path) -> dict[str, str | int]:
    config = load_config(config_path)
    root = get_project_root()
    dataset, manifest = build_analytical_dataset(root, config)
    dataset_path, manifest_path = save_processed_outputs(root, config, dataset, manifest)
    return {
        "dataset_path": str(dataset_path),
        "manifest_path": str(manifest_path),
        "row_count": int(len(dataset)),
    }


def main() -> None:
    args = parse_args()
    result = run_preprocessing(args.config)
    print(
        "Preprocessing completed successfully. "
        f"Rows: {result['row_count']}. Dataset: {result['dataset_path']}. "
        f"Manifest: {result['manifest_path']}"
    )


if __name__ == "__main__":
    main()
