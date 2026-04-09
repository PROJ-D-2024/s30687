# Data

This directory keeps raw inputs separate from generated outputs.

## Structure

- `raw/` - source files placed here without manual edits
- `processed/` - datasets created by the preprocessing code

## Rules

1. Raw files should stay unchanged after download.
2. Cleaning and merging should happen through the code in `src/`.
3. Processed outputs should be reproducible from the same raw inputs and config.
4. The processed dataset should expose the variables needed by the configured F0 and F1 experiments.

## Current input scope

The committed sample bundle consists of:

- `data/raw/sample_gp_practice_population_demographics.csv`
- `data/raw/sample_gp_practice_supporting_inputs.csv`

Together these files are enough to build the processed dataset and train both configured experiments without inventing missing target values during the normal documented run.

The project still contains an optional placeholder fallback in code for private-data scenarios, but that fallback is disabled in the default config and is not the primary reproducibility path documented for Assignment 4.

## Expected raw sources in the final version

- GP practice population and demographic data
- GP workforce or availability data
- hospital use or admissions outcome data
- optional deprivation or regional control variables
