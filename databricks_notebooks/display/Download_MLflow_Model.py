# Databricks notebook source
# MAGIC %md ## Download MLflow Model
# MAGIC
# MAGIC Download an MLflow model artifacts from a model URI such as:
# MAGIC * `models:/Sklearn_Wine_ONNX/production`
# MAGIC * `models:/Sklearn_Wine_ONNX/1`
# MAGIC * `runs:/dfec96c410ef4d3d956bc2afcce8f1a9/onnx-model`

# COMMAND ----------

# MAGIC %run ../Common

# COMMAND ----------

# MAGIC %md #### Widgets

# COMMAND ----------

dbutils.widgets.text("1. Model URI", "")
model_uri = dbutils.widgets.get("1. Model URI")

dbutils.widgets.text("2. Output directory", "")
output_dir = dbutils.widgets.get("2. Output directory")
output_dir = _from_dbfs(output_dir)
os.environ["OUTPUT_DIR"] = output_dir

print("model_uri:", model_uri)
print("output_dir:", output_dir)

# COMMAND ----------

assert_widget(model_uri, "1. Model URI")
assert_widget(output_dir, "2. Output directory")

# COMMAND ----------

# MAGIC %md #### Download MLflow model

# COMMAND ----------

from mlflow_tools.common.model_download_utils import download_model
local_dir = download_model(model_uri, output_dir)
print("Local downloaded directory:", local_dir)

# COMMAND ----------

# MAGIC %md #### Show results

# COMMAND ----------

# MAGIC %sh
# MAGIC echo "OUTPUT_DIR: $OUTPUT_DIR"
# MAGIC ls -lR $OUTPUT_DIR
