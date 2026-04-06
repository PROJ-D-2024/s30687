# Processed data

This directory stores deterministic outputs created by `python -m src preprocess --config config/base.yaml`.

## Expected outputs

- `gp_practice_analysis_dataset.csv` — analytical table consumed by training.
- `gp_practice_analysis_dataset_manifest.json` — provenance metadata, placeholder usage, and file hashes.

These files are generated locally and ignored by Git to avoid committing derived artifacts.
