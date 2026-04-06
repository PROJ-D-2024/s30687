# Configuration

This directory contains the YAML files that control the pipeline.

## Files

- `base.yaml` - shared settings used by all runs: paths, seed, preprocessing options, data locations, and tracking rules
- `experiment_f0.yaml` - baseline setup for the F0 feature set
- `experiment_f1.yaml` - extended setup for the F1 feature set

## How it works

- each experiment file extends `config/base.yaml`
- the code reads the merged configuration at runtime
- training saves that merged version as `config_snapshot.yaml` inside the run folder

## Traceability

The run folder name is based on:

1. experiment name
2. configuration hash
3. seed

Because of that, the mapping from config file to run folder stays stable as long as the config content and seed do not change.
