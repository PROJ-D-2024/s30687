from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import yaml

from src.utils.io_paths import ensure_directory, resolve_from_root


def build_artifact_paths(root: Path, config: Dict[str, Any], run_slug: str) -> Dict[str, Path]:
    run_dir = ensure_directory(resolve_from_root(Path(config["paths"]["reports_dir"]) / "runs" / run_slug, root))
    model_dir = ensure_directory(resolve_from_root(Path(config["paths"]["models_dir"]) / run_slug, root))
    return {
        "run_dir": run_dir,
        "metrics_path": run_dir / "metrics.json",
        "metadata_path": run_dir / "metadata.json",
        "config_snapshot_path": run_dir / "config_snapshot.yaml",
        "model_path": model_dir / "model.joblib",
        "registry_path": resolve_from_root(config["paths"]["tracking_registry_path"], root),
    }


def write_json(path: Path, payload: Dict[str, Any] | List[Dict[str, Any]]) -> None:
    ensure_directory(path.parent)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def write_yaml(path: Path, payload: Dict[str, Any]) -> None:
    ensure_directory(path.parent)
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


def upsert_registry(registry_path: Path, record: Dict[str, Any]) -> None:
    ensure_directory(registry_path.parent)
    existing_records: List[Dict[str, Any]] = []
    if registry_path.exists():
        existing_records = json.loads(registry_path.read_text(encoding="utf-8"))

    filtered_records = [item for item in existing_records if item.get("run_slug") != record["run_slug"]]
    filtered_records.append(record)
    filtered_records.sort(key=lambda item: (item["experiment_name"], item["run_slug"]))
    write_json(registry_path, filtered_records)