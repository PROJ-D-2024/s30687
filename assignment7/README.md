# Assignment 7 - Baseline Models

This folder implements the Assignment 7 baseline modeling stage for the GP hospital utilization thesis project.
The main modeling code is in `baseline_models.ipynb` so the experimental flow can be inspected as a notebook instead of a long script.

The implementation keeps the assumptions from Assignments 1-6:

- research question: whether GP practice demographic structure improves explanation of hospital service use in Scotland beyond practice size and GP availability
- target: `hospital_use_per_1000`
- F0 features: `log1p(AllAges)` and `gp_availability`
- F1 features: F0 plus `share_age_65_plus`, `share_female`, `deprivation_index`, `HB`, and `HSCP`
- metrics: R2, RMSE, MAE
- seed: `42`
- leakage control: PracticeCode-aware holdout and group-aware CV on the training partition

The notebook reads the Assignment 4 raw sample bundle from `assignment4/data/raw/` and writes outputs to `assignment7/outputs/`.

## Run

From the repository root:

```powershell
.\.venv\Scripts\python.exe assignment7\run_baselines.py
.\.venv\Scripts\python.exe assignment7\generate_analysis_docx.py
```

`run_baselines.py` executes the code cells from `baseline_models.ipynb`. The repository-level `.venv` contains the modeling, notebook, EDA, and DOCX dependencies needed for Assignments 4-7.

## Outputs

- `outputs/metrics_table.csv`
- `outputs/metrics_table.json`
- `outputs/model_comparison.csv`
- `outputs/model_comparison.json`
- `outputs/holdout_predictions.csv`
- `outputs/split_assignments.csv`
- `outputs/run_metadata.json`
- `outputs/full_model_results.json`
- `assignment7_baseline_models_analysis.docx`

The committed repository sample is intentionally tiny and synthetic, so the generated metrics are methodological smoke-test results rather than substantive thesis findings. The same protocol should be rerun on the full Public Health Scotland analytical table when it is available.
