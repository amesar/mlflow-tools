# Databricks notebook source
# MAGIC %md ### Dump registered model details
# MAGIC 
# MAGIC Overview
# MAGIC * Dump registered in JSON or YAML
# MAGIC 
# MAGIC Widgets
# MAGIC * 1. Model - registered model name
# MAGIC * 2. Show version runs - show details of the version runs
# MAGIC * 3. Display format - JSON or YAML
# MAGIC * 4. Output JSON file

# COMMAND ----------

# MAGIC %run ./Common

# COMMAND ----------

dbutils.widgets.text("1. Model", "")
model = dbutils.widgets.get("1. Model")
dbutils.widgets.dropdown("2. Show version runs", "yes", ["yes","no"])
dump_runs = dbutils.widgets.get("2. Show version runs") == "yes"
dbutils.widgets.dropdown("3. Format","json", ["json", "yaml"])
format = dbutils.widgets.get("3. Format")
dbutils.widgets.text("4. Output JSON file", "")
output_file = dbutils.widgets.get("4. Output JSON file")

assert_widget(model, "Missing '1. Model' widget")
 
print("model:", model)
print("dump_runs:", dump_runs)
print("format:", format)
print("output_file:", output_file)

# COMMAND ----------

from mlflow_tools.display import dump_model

dct = dump_model.dump(model, 
                      dump_runs=dump_runs, 
                      format=format)

# COMMAND ----------

write_file(dct, output_file, format)

# COMMAND ----------

# MAGIC %md ### Show all model versions
# MAGIC 
# MAGIC * Show all model versions from the [MlflowClient.search_model_versions](https://mlflow.org/docs/latest/python_api/mlflow.client.html#mlflow.client.MlflowClient.search_model_versions) method.
# MAGIC * Note these are all versions, not just the "latest" stage versions.

# COMMAND ----------

from mlflow_tools.display.list_model_versions import to_pandas_dataframe 
pdf = to_pandas_dataframe(model)
df = spark.createDataFrame(pdf)
display(df)

# COMMAND ----------

