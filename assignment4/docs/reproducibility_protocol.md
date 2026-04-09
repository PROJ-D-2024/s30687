# Reproducibility protocol

## 1. Purpose

This document describes the rules used to rerun the Assignment 4 pipeline in a consistent way. The main idea is simple: the same input data and the same configuration should lead to the same processed dataset and the same experiment artifact locations.

## 2. Environment

- Python version: **3.11.9**
- Environment files: `requirements.txt` and `environment.yml`
- Reference machine used for validation:
  - OS: Windows 11
  - CPU: AMD Ryzen AI 9 HX 370 w/ Radeon 890M
  - RAM: 32 GB
  - GPU: AMD Radeon(TM) 890M Graphics

The current pipeline runs on CPU, so the GPU is not required.

## 3. Execution rules

- run commands from the project root
- use `python -m src <command> --config <file>` as the standard entry point
- keep all paths relative to the Assignment 4 project root (`assignment4/`)
- define experiment differences in YAML config files instead of editing code

## 4. Seed handling

- the global seed is stored in `config/base.yaml`
- NumPy and Python randomness are fixed before training
- `train_test_split` and `KFold` use the configured seed
- run folder names depend on experiment name, config hash, and seed

For the current CPU-only preprocessing and linear models, this is enough to make reruns stable in normal use. Small numeric differences across platforms are still theoretically possible.

## 5. Data handling policy

- raw data stays in `data/raw/`
- processed data is written to `data/processed/`
- cleaning and feature derivation are script-based
- imputers and encoders are fitted inside the training pipeline, not on the full dataset beforehand

### Current input bundle

The shared Assignment 4 package includes a tiny synthetic raw-data bundle:

- `data/raw/sample_gp_practice_population_demographics.csv`
- `data/raw/sample_gp_practice_supporting_inputs.csv`

These files are sufficient for the standard documented rerun. The processed-data manifest records both input files and their hashes.

### Optional placeholder fallback

If the supporting input table is intentionally removed and `mock_data.enabled` is switched on, preprocessing can still generate deterministic placeholder values for `gp_availability`, `deprivation_index`, and `hospital_use_per_1000`. That path is kept only as a temporary fallback and is disabled in the default config used for reproducibility.

## 6. Traceability requirements

Each training run should leave behind enough information to identify exactly what was executed. In this repository that means saving:

- `metrics.json`
- `metadata.json`
- `config_snapshot.yaml`
- `model.joblib`
- an entry in `reports/experiment_registry.json`

The metadata should make it possible to link a result to:

- experiment name
- feature set
- model type
- seed
- configuration file and config hash
- processed dataset hash
- git commit hash
- Python and package information

## 7. Standard rerun procedure

1. Create the Python 3.11.9 environment from `requirements.txt` or `environment.yml`.
2. Move into `assignment4/`.
3. Confirm that `data/raw/sample_gp_practice_population_demographics.csv` and `data/raw/sample_gp_practice_supporting_inputs.csv` are present.
4. Run `python -m src preprocess --config config/base.yaml`.
5. Run `python -m src train --config config/experiment_f0.yaml`.
6. Inspect `reports/experiment_registry.json` and `reports/runs/<run_slug>/`.
7. Read stored results with `python -m src evaluate --config config/experiment_f0.yaml`.
8. Optionally repeat training/evaluation for `config/experiment_f1.yaml`.

## 8. Quick repeatability check

Run the same training command again with the same config. The repository should produce the same `run_slug`, write to the same run folder, and keep the saved metrics consistent.
