# Basic MLflow Tools 

## Overview


Model version validation tools.

* [Compare model versions](xx) - Compares a version from two registered models
* [Check model version](xx) - Checks a model version to ensure its cached model == run model

## Compare 

Compares a version from two registered models

Compare the MLflow models backing a registered model version.


```
python -um mlflow_export_import.tools.compare_model_versions \
  --config-file config.yaml \
  --compare-run-models \
  --compare-reg-models" \
  --download-dir scratch \
  --use-deprecated-download-artifacts
```

config.yaml
```
tracking_server_01:
  host: databricks://e2_demo
  model: Sklearn_Wine
  version_or_stage: staging
  native_model: model.pkl
tracking_server_01:
  host: databricks://e2_dogfood
  model: Sklearn_Wine_Imported
  version_or_stage: staging
  native_model: model.pkl
```

**Options**

```
python -m mlflow_tools.tools.check.compare_model_versions --help

  Compare the MLflow models backing a registered model version. 

Options:
  --config-file TEXT    Configuration file  [required]
  --download-dir TEXT   Download directory for artifacts  [required]
  --compare-run-models  Compare run models
  --compare-reg-models  Compare registered models
  --verbose             Verbose
```

## Check model version  - XX

Checks a model version to ensure its cached model == run model.

