# Reproducibility Protocol

## 1. Purpose

This protocol defines how experiments are executed so that results can be reproduced, audited, and linked to a specific state of code and configuration.

## 2. Environment specification

- Python version: **3.11.9**
- Environment files: `requirements.txt` and `environment.yml`
- Reference hardware used for validation:
  - OS: Windows 11
  - CPU: AMD Ryzen AI 9 HX 370 w/ Radeon 890M
  - RAM: 30.62 GB
  - GPU: AMD Radeon(TM) 890M Graphics (not required by the pipeline)

## 3. Random seed handling

- Global seed is defined in configuration files.
- NumPy random seed is fixed before training.
- `train_test_split` and `KFold` use the configured seed.
- Output folder names are deterministic because they depend on the merged config hash and seed.

## 4. Determinism considerations

Determinism is strongest for the current preprocessing, train/test split generation, cross-validation split generation, OLS, and Ridge regression on CPU.

Minor numerical differences can still occur across systems or library builds.

## 5. Path and file management

- No absolute hard-coded paths are allowed.
- All paths are resolved relative to the project root.
- Inputs and outputs are defined via configuration.
- The project exposes one command entry point: `python -m src <command> --config <file>`.

## 6. Experiment traceability

Each experiment should record at least:

- run slug
- timestamp
- experiment name
- feature set (`F0` or `F1`)
- model type
- random seed
- evaluation metrics
- configuration file used
- git commit hash
- processed dataset hash
- Python/package versions

The deterministic run folder is:

```text
reports/runs/<experiment-name>__cfg-<hash>__seed-<seed>/
```

The top-level registry file `reports/experiment_registry.json` provides the direct mapping from configuration to result artifact locations.

## 7. Version control rules

- Git is the source of truth for code state.
- Results quoted in the thesis must be traceable to a specific repository version.
- Major methodological changes should be documented through meaningful commits.

## 8. Data handling policy

- Raw data files remain unchanged after acquisition.
- Cleaning, merging, and feature derivation must be script-based.
- Missing value rules must be documented and consistently applied.
- Imputation must be fitted only on training data for evaluation workflows.

### Current limitation and placeholder rule

The repository currently ships only the demographics workbook needed for the scaffolded preprocessing run. The following real thesis tables are still missing from the distributable repository:

- hospital utilization outcome,
- GP workforce / availability,
- deprivation or similar control variables.

To keep Assignment 4 reproducible end-to-end, preprocessing generates deterministic placeholder columns for these missing variables and records that fact in `data/processed/gp_practice_analysis_dataset_manifest.json`.

## 9. Reproduction checklist

1. Create the Python 3.11.9 environment from `requirements.txt` or `environment.yml`.
2. Place `gp_practice_population_demographics_merged.xlsx` in `data/raw/`.
3. Run `python -m src preprocess --config config/base.yaml`.
4. Run `python -m src train --config config/experiment_f0.yaml`.
5. Run `python -m src train --config config/experiment_f1.yaml`.
6. Inspect `reports/experiment_registry.json`.
7. Run `python -m src evaluate --config config/experiment_f0.yaml` and `python -m src evaluate --config config/experiment_f1.yaml`.
8. Re-run the same experiment and verify that `metrics.json` in the same deterministic run folder stays unchanged.
