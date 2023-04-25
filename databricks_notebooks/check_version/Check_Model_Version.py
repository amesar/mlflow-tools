# Databricks notebook source
# MAGIC %md ## Check Model Version
# MAGIC 
# MAGIC Checks if model version run model artifact matches the cached model registry model.

# COMMAND ----------

# MAGIC %md #### Setup

# COMMAND ----------

# MAGIC %run ../Common

# COMMAND ----------

# MAGIC %md #### Widgets

# COMMAND ----------

dbutils.widgets.text("1. Registered model", "")
model_name = dbutils.widgets.get("1. Registered model")

dbutils.widgets.text("2. Version or stage", "")
version_or_stage = dbutils.widgets.get("2. Version or stage")

print("model_name:", model_name)
print("version_or_stage:", version_or_stage)

# COMMAND ----------

assert_widget(model_name, "1. Registered model")
assert_widget(version_or_stage, "2. Version or stage")

# COMMAND ----------

# MAGIC %md #### Download scratch directory

# COMMAND ----------

download_dir = "/tmp/mlflow_tools/check_version"
import shutil
shutil.rmtree(download_dir, ignore_errors=True)

# COMMAND ----------

# MAGIC %md #### Run version check

# COMMAND ----------

from mlflow_tools.check_version.check_model_version import check_version
res = check_version(
    model_name = model_name,
    version_or_stage = version_or_stage,
    download_dir = download_dir
)
res

# COMMAND ----------

# MAGIC %md #### Show result

# COMMAND ----------

print("Comparison result:", res["Comparison"]["equals"])
