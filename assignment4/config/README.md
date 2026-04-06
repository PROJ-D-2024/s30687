# Configuration layout

This directory separates shared configuration from experiment-specific overrides.

## Files

- `base.yaml` — global paths, preprocessing defaults, seed, dependency assumptions, and tracking conventions.
- `experiment_f0.yaml` — baseline experiment (`F0`) using practice size and GP availability proxy.
- `experiment_f1.yaml` — extended experiment (`F1`) adding demographic structure and controls.

## Naming convention

- `experiment_<feature_set>.yaml` defines one reproducible experiment.
- Each experiment extends `config/base.yaml`.
- The training command stores a snapshot of the merged configuration next to the generated metrics.

## Traceability rule

The folder name in `reports/runs/` is derived from:

1. experiment name,
2. merged configuration hash,
3. seed.

This makes the mapping `config -> run folder -> metrics/model` deterministic.
