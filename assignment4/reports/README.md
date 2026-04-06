# Reports and experiment outputs

Generated experiment outputs are written here.

## Expected generated structure

```text
reports/
├── experiment_registry.json
└── runs/
    └── <run_slug>/
        ├── config_snapshot.yaml
        ├── metadata.json
        └── metrics.json
```

## Traceability rule

- `experiment_registry.json` stores the deterministic mapping between configuration file, run slug, metrics location, and model artifact location.
- Each run folder contains a frozen configuration snapshot and metadata with git commit, dataset hash, and Python/package versions.
- Results are ignored by Git because they are reproducible local artifacts.
