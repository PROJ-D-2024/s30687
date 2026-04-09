from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Tuple

import numpy as np
import pandas as pd

from src.utils.io_paths import ensure_directory, resolve_from_root
from src.utils.reproducibility import file_sha256, utc_now_iso

REQUIRED_DEMOGRAPHICS_COLUMNS = [
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

SUPPORTING_INPUT_COLUMNS = [
    "Date",
    "PracticeCode",
    "gp_availability",
    "deprivation_index",
    "hospital_use_per_1000",
]


def _read_tabular_input(path: Path, sheet_name: str | None = None) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path, sheet_name=sheet_name, engine="openpyxl")
    if suffix == ".csv":
        return pd.read_csv(path)

    raise ValueError(
        "Unsupported raw input format. Expected one of: .csv, .xlsx, .xls. "
        f"Received: {path.name}"
    )


def load_demographics_table(root: Path, config: Dict[str, Any]) -> Tuple[pd.DataFrame, Path]:
    raw_path = resolve_from_root(
        Path(config["paths"]["raw_data_dir"]) / config["data"]["demographics_file"],
        root,
    )
    if not raw_path.exists():
        raise FileNotFoundError(
            "Missing raw demographics input. Expected file: "
            f"{raw_path}. Place it in data/raw/ and rerun preprocessing."
        )

    dataframe = _read_tabular_input(raw_path, sheet_name=config["data"].get("demographics_sheet"))
    missing_columns = sorted(set(REQUIRED_DEMOGRAPHICS_COLUMNS) - set(dataframe.columns))
    if missing_columns:
        raise ValueError(f"Raw demographics file is missing required columns: {missing_columns}")

    return dataframe, raw_path


def load_supporting_inputs(root: Path, config: Dict[str, Any]) -> Tuple[pd.DataFrame | None, Path | None]:
    supporting_file = config["data"].get("supporting_inputs_file")
    if not supporting_file:
        return None, None

    supporting_path = resolve_from_root(Path(config["paths"]["raw_data_dir"]) / supporting_file, root)
    if not supporting_path.exists():
        if config["mock_data"].get("enabled", False):
            return None, supporting_path
        raise FileNotFoundError(
            "Missing supporting raw input table. Expected file: "
            f"{supporting_path}. Place it in data/raw/ and rerun preprocessing."
        )

    dataframe = _read_tabular_input(supporting_path)
    missing_columns = sorted(set(SUPPORTING_INPUT_COLUMNS) - set(dataframe.columns))
    if missing_columns:
        raise ValueError(f"Supporting input file is missing required columns: {missing_columns}")

    return dataframe, supporting_path


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
    supporting_dataframe, supporting_path = load_supporting_inputs(root, config)
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

    placeholder_columns: list[str] = []
    placeholder_reason: str | None = None
    if supporting_dataframe is not None:
        supporting_dataframe["Date"] = pd.to_datetime(supporting_dataframe["Date"])
        merge_columns = list(config["data"].get("id_columns", ["Date", "PracticeCode"]))
        dataset = dataset.merge(
            supporting_dataframe[SUPPORTING_INPUT_COLUMNS],
            on=merge_columns,
            how="left",
            validate="1:1",
        )
        missing_support_rows = dataset[SUPPORTING_INPUT_COLUMNS[2:]].isna().any(axis=1)
        if missing_support_rows.any():
            missing_keys = dataset.loc[missing_support_rows, merge_columns].head(5).to_dict(orient="records")
            raise ValueError(
                "Supporting inputs did not cover all analytical rows. "
                f"Example missing keys: {missing_keys}"
            )
    dataset = dataset.sort_values(["Date", "PracticeCode"]).reset_index(drop=True)

    if supporting_dataframe is None and config["mock_data"]["enabled"]:
        dataset = _derive_placeholder_columns(dataset)
        placeholder_columns = [
            "gp_availability",
            "deprivation_index",
            config["data"]["target_column"],
        ]
        placeholder_reason = (
            "Real hospital use, GP workforce, and deprivation raw tables are not present in the configured input bundle. "
            "Deterministic placeholder columns are generated only as an optional fallback for Assignment 4."
        )
    elif supporting_dataframe is None:
        raise ValueError(
            "The configured run requires supporting inputs with gp_availability, deprivation_index, and the target column. "
            "Either provide data/supporting_inputs_file or enable mock_data as a fallback."
        )

    dataset["Date"] = dataset["Date"].dt.strftime("%Y-%m-%d")
    input_files = [
        {
            "role": "demographics",
            "file_name": raw_path.name,
            "sha256": file_sha256(raw_path),
        }
    ]
    if supporting_dataframe is not None and supporting_path is not None:
        input_files.append(
            {
                "role": "supporting_inputs",
                "file_name": supporting_path.name,
                "sha256": file_sha256(supporting_path),
            }
        )

    manifest = {
        "created_at_utc": utc_now_iso(),
        "input_file": raw_path.name,
        "input_file_sha256": file_sha256(raw_path),
        "input_files": input_files,
        "input_sheet": config["data"]["demographics_sheet"],
        "row_count": int(len(dataset)),
        "column_count": int(len(dataset.columns)),
        "columns": list(dataset.columns),
        "placeholder_columns": placeholder_columns,
        "placeholder_reason": placeholder_reason,
        "used_placeholder_fallback": bool(placeholder_columns),
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