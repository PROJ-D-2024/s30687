from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
from sklearn.model_selection import KFold, cross_validate, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.utils.io_paths import resolve_from_root
from src.utils.reproducibility import file_sha256


def load_processed_dataset(root: Path, config: Dict[str, Any]) -> Tuple[pd.DataFrame, Path]:
    dataset_path = resolve_from_root(config["paths"]["processed_dataset_path"], root)
    if not dataset_path.exists():
        raise FileNotFoundError(
            f"Processed dataset not found: {dataset_path}. Run preprocessing before training."
        )

    dataframe = pd.read_csv(dataset_path, parse_dates=["Date"])
    dataframe = dataframe.sort_values(["Date", "PracticeCode"]).reset_index(drop=True)
    return dataframe, dataset_path


def build_estimator(config: Dict[str, Any]) -> Any:
    model_type = config["model"]["type"].lower()
    params = dict(config["model"].get("params", {}))

    if model_type == "ols":
        return LinearRegression(**params)
    if model_type == "ridge":
        return Ridge(**params)

    raise ValueError(f"Unsupported model type: {config['model']['type']}")


def build_training_pipeline(
    config: Dict[str, Any],
    numeric_features: List[str],
    categorical_features: List[str],
) -> Pipeline:
    numeric_steps: List[Tuple[str, Any]] = [
        ("imputer", SimpleImputer(strategy=config["preprocessing"]["numeric_imputation"])),
    ]
    if config["preprocessing"].get("scale_for_linear_models", False):
        numeric_steps.append(("scaler", StandardScaler()))

    transformers: List[Tuple[str, Any, List[str]]] = [
        ("numeric", Pipeline(steps=numeric_steps), numeric_features),
    ]
    if categorical_features:
        categorical_pipeline = Pipeline(
            steps=[
                (
                    "imputer",
                    SimpleImputer(strategy=config["preprocessing"].get("categorical_imputation", "most_frequent")),
                ),
                ("encoder", OneHotEncoder(handle_unknown="ignore")),
            ]
        )
        transformers.append(("categorical", categorical_pipeline, categorical_features))

    preprocessor = ColumnTransformer(transformers=transformers, remainder="drop")
    return Pipeline(steps=[("preprocessor", preprocessor), ("model", build_estimator(config))])


def _calculate_regression_metrics(y_true: pd.Series, y_pred: np.ndarray) -> Dict[str, float]:
    return {
        "r2": round(float(r2_score(y_true, y_pred)), 6),
        "rmse": round(float(root_mean_squared_error(y_true, y_pred)), 6),
        "mae": round(float(mean_absolute_error(y_true, y_pred)), 6),
    }


def run_experiment(root: Path, config: Dict[str, Any]) -> Dict[str, Any]:
    dataset, dataset_path = load_processed_dataset(root, config)
    numeric_features = list(config["features"].get("numeric", []))
    categorical_features = list(config["features"].get("categorical", []))
    target_column = config["data"]["target_column"]

    required_columns = set(numeric_features + categorical_features + [target_column])
    missing_columns = sorted(required_columns - set(dataset.columns))
    if missing_columns:
        raise ValueError(f"Processed dataset is missing required columns for training: {missing_columns}")

    features = dataset[numeric_features + categorical_features].copy()
    target = dataset[target_column].astype(float)
    seed = int(config["project"]["random_seed"])
    test_size = float(config["data"]["test_size"])

    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=test_size,
        random_state=seed,
        shuffle=True,
    )

    training_pipeline = build_training_pipeline(config, numeric_features, categorical_features)
    training_pipeline.fit(x_train, y_train)

    predictions = training_pipeline.predict(x_test)
    holdout_metrics = _calculate_regression_metrics(y_test, predictions)

    cv = cross_validate(
        training_pipeline,
        features,
        target,
        cv=KFold(n_splits=int(config["data"]["n_splits_cv"]), shuffle=True, random_state=seed),
        scoring={
            "r2": "r2",
            "rmse": "neg_root_mean_squared_error",
            "mae": "neg_mean_absolute_error",
        },
        return_train_score=False,
    )

    cv_metrics = {
        "folds": int(config["data"]["n_splits_cv"]),
        "mean_r2": round(float(np.mean(cv["test_r2"])), 6),
        "std_r2": round(float(np.std(cv["test_r2"], ddof=1)), 6),
        "mean_rmse": round(float(-np.mean(cv["test_rmse"])), 6),
        "std_rmse": round(float(np.std(-cv["test_rmse"], ddof=1)), 6),
        "mean_mae": round(float(-np.mean(cv["test_mae"])), 6),
        "std_mae": round(float(np.std(-cv["test_mae"], ddof=1)), 6),
    }

    preview = pd.DataFrame(
        {
            "actual": y_test.reset_index(drop=True).head(10),
            "predicted": pd.Series(predictions).head(10),
        }
    )

    return {
        "pipeline": training_pipeline,
        "dataset_path": dataset_path,
        "dataset_sha256": file_sha256(dataset_path),
        "metrics": {
            "primary_metric": "holdout_rmse",
            "holdout": holdout_metrics,
            "cross_validation": cv_metrics,
            "dataset": {
                "row_count": int(len(dataset)),
                "train_rows": int(len(x_train)),
                "test_rows": int(len(x_test)),
                "numeric_features": numeric_features,
                "categorical_features": categorical_features,
                "target_column": target_column,
            },
            "prediction_preview": preview.round(6).to_dict(orient="records"),
        },
    }