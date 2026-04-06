# Reports and experiment outputs

This directory stores the files produced during training.

## Expected structure

```text
reports/
├── experiment_registry.json
└── runs/
    └── <run_slug>/
        ├── config_snapshot.yaml
        ├── metadata.json
        └── metrics.json
```

## What is stored here

- `experiment_registry.json` links configs to run folders and saved artifacts
- each run folder keeps the frozen config, metadata, and metrics for one experiment run
- these files are generated locally and are not treated as hand-edited documentation
