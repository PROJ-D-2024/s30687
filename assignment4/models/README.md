# Models

Trained model artifacts are saved locally under deterministic run-specific folders such as:

- `models/<run_slug>/model.joblib`

Large or confidential models should remain outside Git. The corresponding run metadata in `reports/` must still indicate where the model came from and which configuration generated it.
