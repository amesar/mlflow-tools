# Databricks notebook source
# MAGIC %md ### Dump registered model details
# MAGIC 
# MAGIC Overview
# MAGIC * Dump registered as JSON or YAML
# MAGIC 
# MAGIC Widgets
# MAGIC * `1. Model` - registered model name
# MAGIC * `2. Show version runs` - show details of the version runs
# MAGIC * `3. Show permissions` - show run data if showing runs
# MAGIC * `4. Display format` - JSON or YAML
# MAGIC * `5. Output JSON file`

# COMMAND ----------

# MAGIC %run ../Common

# COMMAND ----------

dbutils.widgets.text("1. Model", "")
model = dbutils.widgets.get("1. Model")

dbutils.widgets.dropdown("2. Show version runs", "yes", ["yes","no"])
dump_runs = dbutils.widgets.get("2. Show version runs") == "yes"

dbutils.widgets.dropdown("3. Show permissions","no",["yes","no"])
show_permissions = dbutils.widgets.get("3. Show permissions") == "yes"

dbutils.widgets.dropdown("4. Format","json", ["json", "yaml"])
format = dbutils.widgets.get("4. Format")

dbutils.widgets.text("5. Output JSON file", "")
output_file = dbutils.widgets.get("5. Output JSON file")
 
print("model:", model)
print("dump_runs:", dump_runs)
print("show_permissions:", show_permissions)
print("format:", format)
print("output_file:", output_file)

# COMMAND ----------

assert_widget(model, "Missing '1. Model' widget")

# COMMAND ----------

from mlflow_tools.display import dump_model

dct = dump_model.dump(
    model_name = model, 
    show_permissions = show_permissions,
    dump_runs = dump_runs, 
    format = format
)

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


