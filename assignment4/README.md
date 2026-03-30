# Assignment 4 — Reproducibility and Code Organization

This folder contains a reproducible and modular project scaffold for the engineering thesis topic:

**Can demographic structure of GP practice populations improve the explanation of variation in hospital service use in Scotland compared with a baseline model based only on practice size and GP availability?**

The structure and design below are consistent with the experimental plan defined in Assignment 3.

## Project structure

```text
assignment4/
├── config/
│   ├── base.yaml
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
│   ├── config_loader.py
│   ├── evaluate.py
│   ├── preprocess.py
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

## Installation

### Option 1 — using `venv`

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Option 2 — using Conda

```bash
conda env create -f environment.yml
conda activate thesis-assignment4
```

## Python version

- Recommended: **Python 3.11**

## Hardware assumptions

This project is designed for a standard personal computer:

- CPU: 4+ logical cores
- RAM: 8 GB minimum, 16 GB recommended
- GPU: not required

## Pipeline stages

1. Data preparation
2. Preprocessing
3. Feature set creation (`F0`, `F1`)
4. Training
5. Evaluation
6. Result storage

## Execution instructions

```bash
python src/preprocess.py --config config/base.yaml
python src/train.py --config config/experiment_f0.yaml
python src/train.py --config config/experiment_f1.yaml
python src/evaluate.py --config config/experiment_f1.yaml
```

## Expected outputs

- processed datasets in `data/processed/`
- artifacts or references in `models/`
- metrics and summaries in `reports/`
- configuration-linked experiment outputs for traceability

## Reproducibility rules

- no hard-coded absolute paths
- configuration-driven experiments
- explicit dependency versions
- fixed random seed in config
- results linked to configuration, timestamp, and model type

See also:

- `docs/reproducibility_protocol.md`
- `docs/technical_description.md`
