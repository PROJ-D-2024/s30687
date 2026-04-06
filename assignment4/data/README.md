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

The current pipeline is built around:

- `data/raw/gp_practice_population_demographics_merged.xlsx`

The real hospital outcome table, GP workforce data, and deprivation controls are still missing from the distributable repository. For that reason, preprocessing generates labeled placeholder columns for:

- `gp_availability`
- `deprivation_index`
- `hospital_use_per_1000`

Those placeholders exist only so the repository can be run and checked end to end. They are not meant to stand in for final thesis results.

## Expected raw sources in the final version

- GP practice population and demographic data
- GP workforce or availability data
- hospital use or admissions outcome data
- optional deprivation or regional control variables
