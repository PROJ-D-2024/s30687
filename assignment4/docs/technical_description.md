# Technical Description

## 1. Architectural objective

The purpose of this repository organization is to support disciplined experimentation for the thesis topic concerning variation in hospital service use between GP practices in Scotland. The technical design follows the logic of Assignment 3: first define a clear baseline model, then test whether demographic information improves explanatory power under controlled experimental conditions.

## 2. Separation of concerns

The project is divided into directories with clearly separated roles:

- `data/` stores input and derived datasets,
- `src/` contains reusable Python modules and executable scripts,
- `config/` stores experiment definitions,
- `models/` stores artifacts or references,
- `reports/` stores evaluation summaries,
- `docs/` stores technical and reproducibility documentation.

This separation reduces the risk of hidden processing steps and improves clarity.

## 3. Pipeline logic

The workflow begins with raw public data sources such as GP list sizes, demographic structure, workforce indicators, and hospital utilization variables. These sources are loaded and validated in preprocessing, then merged into a single analytical table.

Two feature variants are planned:

- **F0**: practice size and GP availability,
- **F1**: F0 plus demographic variables and optional controls.

Models are then evaluated using an 80/20 hold-out split and 5-fold cross-validation, consistent with Assignment 3.

## 4. Modularity of implementation

The code scaffold in `src/` separates configuration loading, preprocessing, training, evaluation, path management, and reproducibility utilities. This makes the project easier to extend while keeping experiments traceable.

## 5. Configuration-driven experimentation

YAML files define common settings, feature sets, and model parameters. This avoids manual editing inside scripts and allows controlled comparison between baseline and extended experiments.

## 6. Reproducibility decisions

The project pins dependency versions, centralizes random seed handling, avoids hard-coded paths, and distinguishes clearly between raw and processed data.

## 7. Summary

The delivered structure creates a professional and reproducible foundation for the implementation phase and is aligned with the methodology defined in Assignment 3.
