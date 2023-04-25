# Databricks notebook source
# MAGIC %md ## Compare Model Versions
# MAGIC 
# MAGIC **Overview**
# MAGIC * Compare two model versions. Check that:
# MAGIC   * The cached registry models are the same pointed to by the `download_uri`.
# MAGIC   * The run models are the same - model artifact pointer to by `version.source`.
# MAGIC * The model versions can be in different workspaces.
# MAGIC * If so, you need to create `~/.databrickscfg` with a profile for the exernal workspace.

# COMMAND ----------

# MAGIC %md #### Setup

# COMMAND ----------

# MAGIC %run ../Common

# COMMAND ----------

# MAGIC %md #### Widgets

# COMMAND ----------

dbutils.widgets.dropdown("1. Compare run model","yes",["yes","no"])
compare_run_model = dbutils.widgets.get("1. Compare run model") == "yes"

dbutils.widgets.dropdown("2. Compare reg model","yes",["yes","no"])
compare_reg_model = dbutils.widgets.get("2. Compare reg model") == "yes"

print("compare_run_model:", compare_run_model)
print("compare_reg_model:", compare_reg_model)

# COMMAND ----------

# MAGIC %md #### Download scratch directory

# COMMAND ----------

download_dir = "/tmp/mlflow_tools/compare_versions"
import shutil
shutil.rmtree(download_dir, ignore_errors=True)

# COMMAND ----------

# MAGIC %md #### Configuration - customize per your needs

# COMMAND ----------

# Change me.

config = {
  "tracking_server_1": {
    "host": "databricks",
    "model": "Sklearn_Wine",
    "version_or_stage": "staging",
    "native_model": "model.pkl"
  },
  "tracking_server_2": {
    "host": "databricks",
    "model": "Sklearn_Wine_Imported",
    "version_or_stage": "staging",
    "native_model": "model.pkl"
  }
}

# COMMAND ----------

# MAGIC %md #### Run version comparison

# COMMAND ----------

from mlflow_tools.check_version.compare_model_versions import compare_versions

res = compare_versions(#
    config = config, 
    skip_compare_run_models = not compare_run_model,
    skip_compare_reg_models = not compare_reg_model,
    download_dir = download_dir
)

# COMMAND ----------

# MAGIC %md #### Show result

# COMMAND ----------

print("Comparison result:", res["Comparison_Summary"])
