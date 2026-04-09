# Assignment 4 - Reproducibility and code organization

This repository contains the Assignment 4 version of the thesis project. The goal at this stage is practical: the code should be easy to inspect, runnable from documented commands, and structured so that later experiments can be repeated without editing scripts by hand.

Research question:

**Can demographic structure of GP practice populations improve the explanation of variation in hospital service use in Scotland compared with a baseline model based only on practice size and GP availability?**

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
│   ├── technical_description.md
│   └── technical_description.pdf
├── models/
├── notebooks/
├── reports/
├── src/
│   ├── cli.py
│   ├── config_loader.py
│   ├── data_pipeline.py
│   ├── evaluate.py
│   ├── modeling.py
│   ├── preprocess.py
│   ├── tracking.py
│   ├── train.py
│   └── utils/
├── environment.yml
└── requirements.txt
```

## What is implemented here

The repository supports two experiment configurations:

- **F0** - baseline model using `AllAges` and `gp_availability`
- **F1** - extended model adding demographic shares, deprivation proxy, and regional categorical variables

The current configs correspond to:

- `config/experiment_f0.yaml` -> OLS baseline
- `config/experiment_f1.yaml` -> Ridge model with the broader feature set

## Data scope

The repository now includes a tiny **synthetic sample bundle** that is sufficient to run the full Assignment 4 pipeline from scratch:

- `data/raw/sample_gp_practice_population_demographics.csv`
- `data/raw/sample_gp_practice_supporting_inputs.csv`

The first file provides the demographic structure per practice and month. The second file provides the supporting variables required by the configured experiments: `gp_availability`, `deprivation_index`, and `hospital_use_per_1000`.

These files are anonymized toy inputs prepared only to prove reproducibility and code organization. They are **not** the real thesis dataset and are not meant to support substantive conclusions. When the full thesis bundle is ready, the files in `data/raw/` can be replaced and the config can be updated without changing the rest of the pipeline.

## Installation

### Option 1 - `venv`

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install --requirement requirements.txt
```

### Option 2 - Conda

```powershell
conda env create -f environment.yml
conda activate thesis-assignment4
```

## Environment used for the documented run

- Python: **3.11.9**
- OS: Windows 11
- CPU: **AMD Ryzen AI 9 HX 370 w/ Radeon 890M**
- RAM: **30.62 GB**
- GPU: **AMD Radeon(TM) 890M Graphics**

The pipeline runs on CPU. A GPU is not required.

## Reproducibility rules

- experiments are defined in YAML files, not by editing code
- all paths are resolved relative to the project root
- one entry point is used for all main stages: `python -m src ...`
- the global seed is stored in `config/base.yaml`
- run folders are derived from experiment name, config hash, and seed
- training outputs are linked to config, dataset hash, git commit, and model artifact

## Pipeline stages

1. Read raw input data.
2. Build the processed analytical dataset.
3. Train the selected experiment.
4. Save metrics, metadata, config snapshot, and model artifact.
5. Read stored results through the evaluation command.

## Commands

Run the project from the `assignment4/` directory:

```powershell
cd assignment4
python -m src preprocess --config config/base.yaml
python -m src train --config config/experiment_f0.yaml
python -m src evaluate --config config/experiment_f0.yaml
```

Optional extended run:

```powershell
python -m src train --config config/experiment_f1.yaml
python -m src evaluate --config config/experiment_f1.yaml
```

## Generated outputs

After preprocessing:

- `data/processed/gp_practice_analysis_dataset.csv`
- `data/processed/gp_practice_analysis_dataset_manifest.json`

After training:

- `reports/runs/<run_slug>/metrics.json`
- `reports/runs/<run_slug>/metadata.json`
- `reports/runs/<run_slug>/config_snapshot.yaml`
- `reports/experiment_registry.json`
- `models/<run_slug>/model.joblib`

One example run artifact folder is committed in the repository so that traceability is visible even before you execute anything locally.

## Reproducing the assignment run from scratch

1. Create the Python 3.11.9 environment.
2. Confirm that the bundled sample files are present in `assignment4/data/raw/`.
3. From `assignment4/`, run:

   ```powershell
   python -m src preprocess --config config/base.yaml
   python -m src train --config config/experiment_f0.yaml
   python -m src evaluate --config config/experiment_f0.yaml
   ```

4. Check that the following files appear:
   - `data/processed/gp_practice_analysis_dataset.csv`
   - `data/processed/gp_practice_analysis_dataset_manifest.json`
   - `reports/runs/<run_slug>/metrics.json`
   - `reports/runs/<run_slug>/metadata.json`
   - `reports/runs/<run_slug>/config_snapshot.yaml`
   - `reports/experiment_registry.json`
5. If needed, run `experiment_f1.yaml` in the same way to inspect the extended configuration.

## Quick repeatability check

If you run the same training command again with the same config and seed, the output should go to the same deterministic run folder. A simple way to check this is to compare the hash of `metrics.json` before and after a rerun.

## Optional placeholder fallback

The code still contains an explicit fallback for situations where only the demographics table is available. That mode is disabled in `config/base.yaml` and should be treated only as a temporary scaffold, not as the default reproducible path.

## Related documentation

- `docs/reproducibility_protocol.md`
- `docs/technical_description.md`
- `docs/technical_description.pdf`
