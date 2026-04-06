# Assignment 4 — Reproducibility and Code Organization

This folder contains the reproducibility-oriented repository setup for the engineering thesis topic:

**Can demographic structure of GP practice populations improve the explanation of variation in hospital service use in Scotland compared with a baseline model based only on practice size and GP availability?**

The structure and design below are consistent with Assignment 3 and now enforce:

- a modular `src/` codebase,
- configuration-driven execution,
- deterministic preprocessing/training/evaluation,
- traceable experiment artifacts in `reports/` and `models/`.

## Project structure

```text
assignment4/
├── config/
│   ├── base.yaml
│   ├── README.md
│   ├── experiment_f0.yaml
│   └── experiment_f1.yaml
├── data/
│   ├── raw/
│   ├── processed/
│   └── README.md
├── docs/
│   ├── reproducibility_protocol.md
│   └── technical_description.md
├── models/
├── notebooks/
├── reports/
├── src/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── config_loader.py
│   ├── data_pipeline.py
│   ├── evaluate.py
│   ├── modeling.py
│   ├── preprocess.py
│   ├── tracking.py
│   ├── train.py
│   └── utils/
│       ├── __init__.py
│       ├── io_paths.py
│       └── reproducibility.py
├── .gitignore
├── environment.yml
├── requirements.txt
└── 04-Reproducibility-and-Code-Organization.md
```

## Research objective

The project is organized to support a controlled comparison between:

- **F0 baseline**: practice size + GP availability
- **F1 extended model**: F0 + demographic structure (especially share of population aged 65+) and additional control variables

The main evaluation goal is to verify whether F1 improves **R²** and reduces **RMSE** relative to F0 under the same split and evaluation protocol.

## Current data scope and placeholder policy

The repository currently contains a demographics workbook as the raw input expected by preprocessing. The real hospital utilization outcome table, GP workforce table, and deprivation controls are **not** distributed in the repository. To keep Assignment 4 reproducible end-to-end, preprocessing creates deterministic placeholder columns for:

- `gp_availability`
- `deprivation_index`
- `hospital_use_per_1000`

These placeholders are explicitly labeled in the processed manifest and are only a technical substitute for repository validation. They must be replaced by real thesis data before reporting final scientific conclusions.

## Installation

### Option 1 — using `venv`

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install --requirement requirements.txt
```

### Option 2 — using Conda

```powershell
conda env create -f environment.yml
conda activate thesis-assignment4
```

## Python version

- Required for the pinned environment: **Python 3.11.9**
- The pipeline was validated locally with `py -3.11`

## Hardware used for the documented run

The repository was prepared and tested on:

- OS: Windows 11
- CPU: **AMD Ryzen AI 9 HX 370 w/ Radeon 890M**
- RAM: **30.62 GB**
- GPU: **AMD Radeon(TM) 890M Graphics**

The pipeline runs on CPU only. GPU is not required.

## Seeds and determinism

- Global seed is set in `config/base.yaml` (`project.random_seed: 42`).
- `random.seed(...)` and `numpy.random.seed(...)` are fixed before training.
- Hold-out split and cross-validation folds use the configured seed.
- Output folder names are deterministic because they depend on experiment name, config hash, and seed.
- Small numerical differences across OS or BLAS builds are still theoretically possible, but the current CPU-only linear models are expected to be stable.

## Pipeline stages

1. Data preparation
2. Preprocessing
3. Feature set creation (`F0`, `F1`)
4. Training
5. Evaluation
6. Result storage

## Execution instructions

Use the single entry point below from the `assignment4/` directory:

```powershell
python -m src preprocess --config config/base.yaml
python -m src train --config config/experiment_f0.yaml
python -m src train --config config/experiment_f1.yaml
python -m src evaluate --config config/experiment_f0.yaml
python -m src evaluate --config config/experiment_f1.yaml
```

## What each stage writes

After preprocessing:

- `data/processed/gp_practice_analysis_dataset.csv`
- `data/processed/gp_practice_analysis_dataset_manifest.json`

After training each experiment:

- `reports/runs/<run_slug>/metrics.json`
- `reports/runs/<run_slug>/metadata.json`
- `reports/runs/<run_slug>/config_snapshot.yaml`
- `reports/experiment_registry.json`
- `models/<run_slug>/model.joblib`

## Expected outputs

- processed dataset and manifest in `data/processed/`
- run-specific metrics and metadata in `reports/runs/`
- registry mapping `config -> run_slug -> metrics/model` in `reports/experiment_registry.json`
- joblib model artifacts in `models/`

## Reproducibility rules

- no hard-coded absolute paths
- configuration-driven experiments via YAML
- one unified entry point: `python -m src ...`
- explicit dependency versions
- fixed random seed in config
- results linked to configuration hash, git commit, dataset hash, and model type

## How to reproduce the documented result from zero

1. Clone the repository.
2. Create the Python 3.11.9 environment from `requirements.txt` or `environment.yml`.
3. Place `gp_practice_population_demographics_merged.xlsx` in `data/raw/`.
4. Run preprocessing.
5. Run baseline F0 training.
6. Run extended F1 training.
7. Inspect metrics with `python -m src evaluate --config ...`.
8. Verify `reports/experiment_registry.json` for the config-to-result mapping.

## Quick reproducibility check

Run the same experiment twice and compare the metrics file hash:

```powershell
python -m src train --config config/experiment_f1.yaml
$metrics = Get-ChildItem .\reports\runs -Recurse -Filter metrics.json |
  Where-Object { $_.FullName -like '*extended-f1-ridge*' } |
  Select-Object -First 1 -ExpandProperty FullName
$hash_before = (Get-FileHash $metrics -Algorithm SHA256).Hash
python -m src train --config config/experiment_f1.yaml
$hash_after = (Get-FileHash $metrics -Algorithm SHA256).Hash
"before=$hash_before"
"after=$hash_after"
```

The metrics content stored under the deterministic `run_slug` should remain unchanged for repeated runs with the same config and seed.

See also:

- `docs/reproducibility_protocol.md`
- `docs/technical_description.md`
- `docs/technical_description.pdf` (if present in your local copy)
