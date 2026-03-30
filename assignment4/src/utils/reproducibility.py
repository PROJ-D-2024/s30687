from __future__ import annotations

import random
from datetime import datetime, timezone
from typing import Any, Dict


def set_global_seed(seed: int) -> None:
    random.seed(seed)


def build_run_metadata(
    experiment_name: str,
    model_type: str,
    feature_set: str,
    seed: int,
    config_path: str,
) -> Dict[str, Any]:
    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "experiment_name": experiment_name,
        "model_type": model_type,
        "feature_set": feature_set,
        "random_seed": seed,
        "config_path": config_path,
    }
