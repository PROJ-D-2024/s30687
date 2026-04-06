# Models

Saved model artifacts are written to run-specific folders such as:

- `models/<run_slug>/model.joblib`

These files are local outputs, not source files. If a model is too large or sensitive to keep in the repository, the matching metadata in `reports/` should still show which run created it.
