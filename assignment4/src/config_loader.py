from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import yaml


def _read_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file) or {}


def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    merged = dict(base)
    for key, value in override.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def load_config(config_path: str | Path) -> Dict[str, Any]:
    path = Path(config_path).resolve()
    config = _read_yaml(path)

    extends = config.pop("extends", None)
    if not extends:
        return config

    base_path = (path.parent.parent / extends).resolve() if not Path(extends).is_absolute() else Path(extends)
    if not base_path.exists():
        base_path = (path.parent / extends).resolve()

    base_config = _read_yaml(base_path)
    return _deep_merge(base_config, config)
