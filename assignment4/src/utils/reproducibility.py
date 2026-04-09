from __future__ import annotations

import hashlib
import json
import os
import platform
import random
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

import numpy as np


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def set_global_seed(seed: int) -> None:
    os.environ.setdefault("PYTHONHASHSEED", str(seed))
    random.seed(seed)
    np.random.seed(seed)


def stable_hash(payload: Any) -> str:
    serialized = json.dumps(payload, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def file_sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def build_run_slug(
    experiment_name: str,
    config: Dict[str, Any],
    config_path: str | Path,
    seed: int,
    project_root: Path,
) -> tuple[str, str]:
    config_path_obj = Path(config_path).resolve()
    try:
        relative_config_path = config_path_obj.relative_to(project_root).as_posix()
    except ValueError:
        relative_config_path = config_path_obj.as_posix()

    config_hash = stable_hash({"config_path": relative_config_path, "config": config})[:12]
    run_slug = f"{slugify(experiment_name)}__cfg-{config_hash}__seed-{seed}"
    return run_slug, config_hash


def get_git_commit_hash(project_root: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(project_root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def get_environment_metadata() -> Dict[str, Any]:
    packages = {}
    try:
        from importlib.metadata import PackageNotFoundError, version
    except ImportError:  # pragma: no cover
        from importlib_metadata import PackageNotFoundError, version  # type: ignore

    for package_name in ["numpy", "pandas", "scikit-learn", "PyYAML", "joblib", "openpyxl"]:
        try:
            packages[package_name] = version(package_name)
        except PackageNotFoundError:
            packages[package_name] = "not-installed"

    return {
        "python_version": sys.version.split(" ")[0],
        "platform": platform.platform(),
        "packages": packages,
    }


def build_run_metadata(
    experiment_name: str,
    model_type: str,
    feature_set: str,
    seed: int,
    config_path: str,
) -> Dict[str, Any]:
    return {
        "timestamp_utc": utc_now_iso(),
        "experiment_name": experiment_name,
        "model_type": model_type,
        "feature_set": feature_set,
        "random_seed": seed,
        "config_path": config_path,
    }
