from __future__ import annotations

import argparse
import json

from config_loader import load_config
from utils.io_paths import get_project_root
from utils.reproducibility import build_run_metadata, set_global_seed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a configured experiment.")
    parser.add_argument("--config", required=True, help="Path to YAML configuration file.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    root = get_project_root()

    seed = int(config["project"]["random_seed"])
    set_global_seed(seed)

    reports_dir = root / config["paths"]["reports_dir"]
    reports_dir.mkdir(parents=True, exist_ok=True)

    metadata = build_run_metadata(
        experiment_name=config["experiment"]["name"],
        model_type=config["model"]["type"],
        feature_set=config["experiment"]["feature_set"],
        seed=seed,
        config_path=args.config,
    )

    result_payload = {
        "metadata": metadata,
        "status": "scaffold",
        "message": "Training scaffold prepared. Connect real dataset loading and model fitting here.",
        "planned_metrics": ["r2", "rmse", "mae"],
    }

    output_file = reports_dir / f"{config['experiment']['name']}_run.json"
    output_file.write_text(json.dumps(result_payload, indent=2), encoding="utf-8")

    print(f"Experiment scaffold saved to: {output_file}")


if __name__ == "__main__":
    main()
