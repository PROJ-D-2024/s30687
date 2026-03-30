# Reproducibility Protocol

## 1. Purpose

This protocol defines how experiments are executed so that results can be reproduced, audited, and linked to a specific state of code and configuration.

## 2. Environment specification

- Python version: **3.11**
- Dependencies: pinned in `requirements.txt` and `environment.yml`
- Hardware target:
  - CPU execution
  - 8 GB RAM minimum
  - GPU not required

## 3. Random seed handling

- Global seed is defined in configuration files.
- NumPy random seed is fixed before training.
- Python hash seed can be set externally when stricter determinism is needed.
- Models supporting `random_state` must receive the configured seed.

## 4. Determinism considerations

Determinism is strongest for train/test split generation, cross-validation split generation, Ridge regression, and Random Forest with fixed `random_state`.

Minor numerical differences can still occur across systems or library builds.

## 5. Path and file management

- No absolute hard-coded paths are allowed.
- All paths are resolved relative to the project root.
- Inputs and outputs are defined via configuration.

## 6. Experiment traceability

Each experiment should record at least:

- timestamp
- experiment name
- feature set (`F0` or `F1`)
- model type
- random seed
- evaluation metrics
- configuration file used

## 7. Version control rules

- Git is the source of truth for code state.
- Results quoted in the thesis must be traceable to a specific repository version.
- Major methodological changes should be documented through meaningful commits.

## 8. Data handling policy

- Raw data files remain unchanged after acquisition.
- Cleaning, merging, and feature derivation must be script-based.
- Missing value rules must be documented and consistently applied.
- Imputation must be fitted only on training data for evaluation workflows.

## 9. Reproduction checklist

1. Create the environment from `requirements.txt` or `environment.yml`
2. Place source data in `data/raw/`
3. Run preprocessing with `config/base.yaml`
4. Run baseline experiment with `config/experiment_f0.yaml`
5. Run extended experiment with `config/experiment_f1.yaml`
6. Compare metrics stored in `reports/`
