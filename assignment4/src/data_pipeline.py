from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Tuple

import numpy as np
import pandas as pd

from src.utils.io_paths import ensure_directory, resolve_from_root
from src.utils.reproducibility import file_sha256, utc_now_iso

REQUIRED_COLUMNS = [
    "Date",
    "PracticeCode",
    "HB",
    "HSCP",
    "Sex",
    "AllAges",
    "Ages0to4",
    "Ages5to14",
    "Ages15to24",
    "Ages25to44",
    "Ages45to64",
    "Ages65to74",
    "Ages75to84",
    "Ages85plus",
]


def load_demographics_table(root: Path, config: Dict[str, Any]) -> Tuple[pd.DataFrame, Path]:
    raw_path = resolve_from_root(
        Path(config["paths"]["raw_data_dir"]) / config["data"]["demographics_file"],
        root,
    )
    if not raw_path.exists():
        raise FileNotFoundError(
            "Missing raw demographics workbook. Expected file: "
            f"{raw_path}. Place it in data/raw/ and rerun preprocessing."
        )

    dataframe = pd.read_excel(
        raw_path,
        sheet_name=config["data"]["demographics_sheet"],
        engine="openpyxl",
    )
    missing_columns = sorted(set(REQUIRED_COLUMNS) - set(dataframe.columns))
    if missing_columns:
        raise ValueError(f"Raw demographics file is missing required columns: {missing_columns}")

    return dataframe, raw_path


def _derive_placeholder_columns(dataset: pd.DataFrame) -> pd.DataFrame:
    practice_code_numeric = pd.to_numeric(dataset["PracticeCode"], errors="coerce").fillna(0).astype(int)
    practice_signal = ((practice_code_numeric % 17) - 8) / 8.0
    hb_codes = pd.Categorical(dataset["HB"]).codes.astype(float)
    hscp_codes = pd.Categorical(dataset["HSCP"]).codes.astype(float)
    month_signal = np.sin(2.0 * np.pi * dataset["Date"].dt.month.astype(float) / 12.0)

    gp_availability = (
        0.40
        + 0.18 * np.log1p(dataset["AllAges"]) / np.log1p(dataset["AllAges"].max())
        + 0.08 * practice_signal
        + 0.25 * dataset["share_age_65_plus"]
    )
    deprivation_index = (
        22.0
        + 4.5 * hb_codes
        + 0.12 * hscp_codes
        + 40.0 * (dataset["share_age_0_14"] - dataset["share_age_65_plus"])
    )
    deprivation_index = np.clip(deprivation_index, 0.0, 100.0)

    hospital_use_per_1000 = (
        35.0
        + 0.0025 * dataset["AllAges"]
        + 110.0 * gp_availability
        + 620.0 * dataset["share_age_65_plus"]
        + 90.0 * dataset["share_female"]
        + 1.75 * deprivation_index
        + 4.0 * month_signal
        + 2.5 * practice_signal
    )

    dataset["gp_availability"] = gp_availability.round(6)
    dataset["deprivation_index"] = deprivation_index.round(6)
    dataset["hospital_use_per_1000"] = hospital_use_per_1000.round(6)
    dataset["target_is_placeholder"] = True
    dataset["source_bundle"] = "demographics-only placeholder proxies for A4 reproducibility"
    return dataset


def build_analytical_dataset(root: Path, config: Dict[str, Any]) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    raw_dataframe, raw_path = load_demographics_table(root, config)
    raw_dataframe["Date"] = pd.to_datetime(raw_dataframe["Date"])

    numeric_columns = [
        "AllAges",
        "Ages0to4",
        "Ages5to14",
        "Ages15to24",
        "Ages25to44",
        "Ages45to64",
        "Ages65to74",
        "Ages75to84",
        "Ages85plus",
    ]
    for column in numeric_columns:
        raw_dataframe[column] = pd.to_numeric(raw_dataframe[column], errors="coerce")

    age_band_columns = [column for column in numeric_columns if column != "AllAges"]
    raw_dataframe[age_band_columns] = raw_dataframe[age_band_columns].fillna(0.0)

    aggregate_label = config["preprocessing"]["keep_sex_aggregate"]
    all_population = raw_dataframe.loc[raw_dataframe["Sex"] == aggregate_label].copy()
    female_population = raw_dataframe.loc[raw_dataframe["Sex"] == "Female", ["Date", "PracticeCode", "AllAges"]].copy()
    female_population = female_population.rename(columns={"AllAges": "female_population"})

    dataset = all_population[
        [
            "Date",
            "PracticeCode",
            "HB",
            "HSCP",
            "AllAges",
            "Ages0to4",
            "Ages5to14",
            "Ages15to24",
            "Ages25to44",
            "Ages45to64",
            "Ages65to74",
            "Ages75to84",
            "Ages85plus",
        ]
    ].merge(
        female_population,
        on=["Date", "PracticeCode"],
        how="left",
        validate="1:1",
    )

    dataset = dataset.loc[dataset["AllAges"].fillna(0) > 0].copy()
    dataset["female_population"] = dataset["female_population"].fillna(dataset["AllAges"] * 0.5)
    dataset["share_age_0_14"] = (dataset["Ages0to4"] + dataset["Ages5to14"]) / dataset["AllAges"]
    dataset["share_age_65_plus"] = (
        dataset["Ages65to74"] + dataset["Ages75to84"] + dataset["Ages85plus"]
    ) / dataset["AllAges"]
    dataset["share_female"] = dataset["female_population"] / dataset["AllAges"]
    dataset = dataset.sort_values(["Date", "PracticeCode"]).reset_index(drop=True)

    if config["mock_data"]["enabled"]:
        dataset = _derive_placeholder_columns(dataset)

    dataset["Date"] = dataset["Date"].dt.strftime("%Y-%m-%d")
    manifest = {
        "created_at_utc": utc_now_iso(),
        "input_file": raw_path.name,
        "input_file_sha256": file_sha256(raw_path),
        "input_sheet": config["data"]["demographics_sheet"],
        "row_count": int(len(dataset)),
        "column_count": int(len(dataset.columns)),
        "columns": list(dataset.columns),
        "placeholder_columns": [
            "gp_availability",
            "deprivation_index",
            config["data"]["target_column"],
        ],
        "placeholder_reason": (
            "Real hospital use, GP workforce, and deprivation raw tables are not present in the repository. "
            "Deterministic placeholder columns are generated only to prove Assignment 4 reproducibility."
        ),
        "mock_data_version": config["mock_data"]["version"],
    }
    return dataset, manifest


def save_processed_outputs(
    root: Path,
    config: Dict[str, Any],
    dataset: pd.DataFrame,
    manifest: Dict[str, Any],
) -> Tuple[Path, Path]:
    dataset_path = resolve_from_root(config["paths"]["processed_dataset_path"], root)
    manifest_path = resolve_from_root(config["paths"]["processed_manifest_path"], root)
    ensure_directory(dataset_path.parent)
    dataset.to_csv(dataset_path, index=False)
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return dataset_path, manifest_path