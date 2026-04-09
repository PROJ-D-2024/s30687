from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib

from src.config_loader import load_config
from src.modeling import run_experiment
from src.tracking import build_artifact_paths, upsert_registry, write_json, write_yaml
from src.utils.io_paths import get_project_root, to_project_relative_path
from src.utils.reproducibility import (
    build_run_metadata,
    build_run_slug,
    get_environment_metadata,
    get_git_commit_hash,
    set_global_seed,
    utc_now_iso,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a configured experiment.")
    parser.add_argument("--config", required=True, help="Path to YAML configuration file.")
    return parser.parse_args()


def run_training(config_path: str | Path) -> dict[str, str]:
    config = load_config(config_path)
    root = get_project_root()

    seed = int(config["project"]["random_seed"])
    set_global_seed(seed)

    training_result = run_experiment(root, config)
    run_slug, config_hash = build_run_slug(
        experiment_name=config["experiment"]["name"],
        config=config,
        config_path=config_path,
        seed=seed,
        project_root=root,
    )
    artifact_paths = build_artifact_paths(root, config, run_slug)
    environment = get_environment_metadata()

    metadata = build_run_metadata(
        experiment_name=config["experiment"]["name"],
        model_type=config["model"]["type"],
        feature_set=config["experiment"]["feature_set"],
        seed=seed,
        config_path=to_project_relative_path(config_path, root),
    )
    metadata.update(
        {
            "created_at_utc": utc_now_iso(),
            "run_slug": run_slug,
            "config_hash": config_hash,
            "experiment_description": config["experiment"]["description"],
            "git_commit": get_git_commit_hash(root),
            "dataset_path": to_project_relative_path(training_result["dataset_path"], root),
            "dataset_sha256": training_result["dataset_sha256"],
            "environment": environment,
            "artifact_locations": {
                "metrics_path": to_project_relative_path(artifact_paths["metrics_path"], root),
                "model_path": to_project_relative_path(artifact_paths["model_path"], root),
                "config_snapshot_path": to_project_relative_path(artifact_paths["config_snapshot_path"], root),
            },
        }
    )

    metrics_payload = training_result["metrics"]
    write_json(artifact_paths["metrics_path"], metrics_payload)
    write_json(artifact_paths["metadata_path"], metadata)
    write_yaml(artifact_paths["config_snapshot_path"], config)

    if config["tracking"].get("save_model", True):
        joblib.dump(training_result["pipeline"], artifact_paths["model_path"])

    registry_record = {
        "run_slug": run_slug,
        "experiment_name": config["experiment"]["name"],
        "feature_set": config["experiment"]["feature_set"],
        "config_path": to_project_relative_path(config_path, root),
        "config_hash": config_hash,
        "metrics_path": to_project_relative_path(artifact_paths["metrics_path"], root),
        "metadata_path": to_project_relative_path(artifact_paths["metadata_path"], root),
        "model_path": to_project_relative_path(artifact_paths["model_path"], root),
        "git_commit": metadata["git_commit"],
        "holdout_r2": metrics_payload["holdout"]["r2"],
        "holdout_rmse": metrics_payload["holdout"]["rmse"],
        "holdout_mae": metrics_payload["holdout"]["mae"],
    }
    upsert_registry(artifact_paths["registry_path"], registry_record)

    return {
        "run_slug": run_slug,
        "metrics_path": str(artifact_paths["metrics_path"]),
        "metadata_path": str(artifact_paths["metadata_path"]),
        "registry_path": str(artifact_paths["registry_path"]),
        "model_path": str(artifact_paths["model_path"]),
    }


def main() -> None:
    args = parse_args()
    result = run_training(args.config)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
