# Assignment 4 technical description

## 1. Purpose of the repository

This repository is the Assignment 4 version of the thesis project. The point of this stage is not to present final scientific results yet, but to put the work into a form that is easy to run, inspect, and repeat.

The thesis question stays the same as in Assignment 3: whether demographic structure helps explain variation in hospital service use across GP practices in Scotland beyond a simpler baseline based on practice size and GP availability. What changes here is the technical setup around that question. Instead of relying on loose scripts or notebook-only work, the project is organized as a small pipeline with documented inputs, configuration files, and saved outputs.

In practical terms, another person should be able to see where raw data belongs, run the main commands from the repository root, and identify which configuration produced a given model and a given metrics file.

## 2. Repository layout

The project is split into a few clear areas:

- `data/raw/` for source files,
- `data/processed/` for datasets created by preprocessing,
- `config/` for shared settings and experiment definitions,
- `src/` for the actual implementation,
- `reports/` for metrics and run metadata,
- `models/` for saved estimators,
- `docs/` for the written documentation.

Inside `src/`, the responsibilities are separated instead of mixed into one script. `data_pipeline.py` handles reading and shaping the input data. `modeling.py` builds the scikit-learn pipeline and calculates metrics. `tracking.py` is responsible for where results are written. The command files `preprocess.py`, `train.py`, and `evaluate.py` are thin wrappers around those reusable modules.

The project also uses one consistent command style:

```text
python -m src <command> --config <file>
```

That keeps execution predictable. It also makes the README and the reproducibility protocol shorter, because all main actions follow the same pattern.

## 3. Data flow and preprocessing

At the moment the pipeline expects one raw workbook in `data/raw/`:

- `gp_practice_population_demographics_merged.xlsx`

The preprocessing code reads the `data` sheet, checks that the required columns exist, parses the `Date` column, and reshapes the workbook into an analytical table with one row per practice and date.

The demographic derivation is straightforward. Rows with `Sex == "All"` provide total population and the age-band counts. Rows with `Sex == "Female"` are merged back in so the pipeline can calculate `share_female`. From those values the code derives the main demographic ratios used later in the experiments:

- `share_age_0_14`
- `share_age_65_plus`
- `share_female`

The current repository does not yet ship the real hospital outcome table, GP workforce data, or deprivation controls. Because of that, `src/data_pipeline.py` creates placeholder columns for:

- `gp_availability`
- `deprivation_index`
- `hospital_use_per_1000`

These placeholders are deterministic, so they let the full project run in a repeatable way, but they are not meant to be treated as real thesis data. The generated manifest in `data/processed/` records that these variables were created as stand-ins. This is important because it makes the limitation explicit instead of hiding it.

## 4. Configuration and experiment setup

The repository uses YAML files to separate implementation from experiment definition.

`config/base.yaml` contains the shared settings: paths, Python version, random seed, preprocessing defaults, output locations, and tracking settings. The experiment files extend that base file and only override what differs between runs.

The current experiments are:

- `experiment_f0.yaml` - baseline feature set, using `AllAges` and `gp_availability`, trained with OLS
- `experiment_f1.yaml` - extended feature set, adding `share_age_65_plus`, `share_female`, `deprivation_index`, and categorical controls `HB` and `HSCP`, trained with Ridge regression

This arrangement matters for two reasons. First, switching from one experiment to another does not require code changes. Second, the exact merged configuration can be saved next to the results, which makes later inspection much easier.

## 5. Training and evaluation logic

The training path is implemented in `src/modeling.py`. It builds a scikit-learn pipeline with separate handling for numeric and categorical features.

For numeric columns, the pipeline applies median imputation and, if enabled, standard scaling. For categorical columns, it applies most-frequent imputation followed by one-hot encoding. The final estimator is chosen from the config and is currently either OLS or Ridge.

The evaluation logic mirrors the plan from Assignment 3:

- 80/20 hold-out split
- 5-fold cross-validation
- metrics: R2, RMSE, and MAE

The code stores both hold-out and cross-validation summaries in `metrics.json`, together with the feature lists and a small prediction preview. The `evaluate` command does not retrain the model. It reads the stored artifacts for the deterministic run folder that matches the given config.

## 6. Traceability and reproducibility

The repository uses a few simple rules to keep runs traceable.

First, the environment is pinned with `requirements.txt` and `environment.yml`, and the documented Python version is 3.11.9. Second, the seed is stored in configuration and is applied before training. Third, the project resolves paths relative to the repository root, so it does not depend on machine-specific absolute paths.

The most visible traceability mechanism is the run folder name. It is derived from the experiment name, configuration hash, and seed. As long as those inputs stay the same, the run slug stays the same as well.

Each training run writes:

- `reports/runs/<run_slug>/metrics.json`
- `reports/runs/<run_slug>/metadata.json`
- `reports/runs/<run_slug>/config_snapshot.yaml`
- `models/<run_slug>/model.joblib`

In addition, `reports/experiment_registry.json` keeps a top-level index of the saved runs. The metadata includes the processed dataset hash, the git commit hash, and environment details. That gives a direct link between reported numbers and the code state that produced them.

## 7. Current limitations

The main limitation of the current repository is data availability, not code structure. The pipeline is ready to accept the real hospital outcome, workforce, and deprivation sources, but those tables are not part of the shared package yet.

When those data sources are available, the placeholder generation in preprocessing should be removed and replaced with the real merge logic. The rest of the project layout can stay the same. That is one of the benefits of the current design: the data layer can be improved without reorganizing commands, configs, or artifact storage.

## 8. Summary

In its current form, the repository does what Assignment 4 is supposed to establish. It separates code, configuration, data, outputs, and documentation; it provides one repeatable way to run preprocessing and training; and it leaves behind enough metadata to connect results to a specific configuration and code state.

The project is still a scaffold, because some real thesis inputs are missing, but the technical foundation is now clear and usable for the next stage of the work.
