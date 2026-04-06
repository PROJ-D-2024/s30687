from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.config_loader import load_config
from src.utils.io_paths import get_project_root, resolve_from_root
from src.utils.reproducibility import build_run_slug


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect experiment outputs.")
    parser.add_argument("--config", required=True, help="Path to YAML configuration file.")
    return parser.parse_args()


def run_evaluation(config_path: str | Path) -> dict[str, object]:
    config = load_config(config_path)
    root = get_project_root()
    seed = int(config["project"]["random_seed"])
    run_slug, _ = build_run_slug(
        experiment_name=config["experiment"]["name"],
        config=config,
        config_path=config_path,
        seed=seed,
        project_root=root,
    )

    metrics_path = resolve_from_root(Path(config["paths"]["reports_dir"]) / "runs" / run_slug / "metrics.json", root)
    metadata_path = resolve_from_root(Path(config["paths"]["reports_dir"]) / "runs" / run_slug / "metadata.json", root)

    if not metrics_path.exists() or not metadata_path.exists():
        raise FileNotFoundError(
            "No traceable report found for this configuration yet. Run training first. "
            f"Expected metrics path: {metrics_path}"
        )

    return {
        "run_slug": run_slug,
        "metrics": json.loads(metrics_path.read_text(encoding="utf-8")),
        "metadata": json.loads(metadata_path.read_text(encoding="utf-8")),
    }


def main() -> None:
    args = parse_args()
    payload = run_evaluation(args.config)
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
