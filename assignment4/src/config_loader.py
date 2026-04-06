from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Dict

import yaml


def _read_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file) or {}


def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    merged = deepcopy(base)
    for key, value in override.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def _resolve_extends_path(path: Path, extends: str) -> Path:
    candidate = Path(extends)
    if candidate.is_absolute():
        return candidate

    for base_dir in (path.parent.parent, path.parent):
        resolved = (base_dir / candidate).resolve()
        if resolved.exists():
            return resolved

    return (path.parent.parent / candidate).resolve()


def load_config(config_path: str | Path) -> Dict[str, Any]:
    path = Path(config_path).resolve()
    config = _read_yaml(path)

    extends = config.pop("extends", None)
    if not extends:
        return config

    base_path = _resolve_extends_path(path, extends)
    base_config = _read_yaml(base_path)
    return _deep_merge(base_config, config)
