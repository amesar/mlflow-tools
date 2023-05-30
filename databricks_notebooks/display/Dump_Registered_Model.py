# Databricks notebook source
# MAGIC %md ### Dump registered model details
# MAGIC
# MAGIC Overview
# MAGIC * Dump registered as JSON or YAML
# MAGIC
# MAGIC Widgets
# MAGIC * `1. Model` - registered model name
# MAGIC * `2. Dump all versions instead of latest versions`
# MAGIC * `3. Dump version runs` - dump details of the version runs
# MAGIC * `4. Dump permissions` - dump run data if showing runs
# MAGIC * `5. Display format` - JSON or YAML
# MAGIC * `6. Output JSON file`

# COMMAND ----------

# MAGIC %run ../Common

# COMMAND ----------

dbutils.widgets.text("1. Model", "")
model = dbutils.widgets.get("1. Model")

dbutils.widgets.dropdown("2. Dump all versions", "no", ["yes","no"])
dump_all_versions = dbutils.widgets.get("2. Dump all versions") == "yes"

dbutils.widgets.dropdown("3. Dump version runs", "yes", ["yes","no"])
dump_runs = dbutils.widgets.get("3. Dump version runs") == "yes"

dbutils.widgets.dropdown("4. Dump permissions", "no", ["yes","no"])
dump_permissions = dbutils.widgets.get("4. Dump permissions") == "yes"

dbutils.widgets.dropdown("5. Show system info", "no", ["yes","no"])
show_system_info = dbutils.widgets.get("5. Show system info") == "yes"

dbutils.widgets.dropdown("6. Format","json", ["json", "yaml"])
format = dbutils.widgets.get("6. Format")

dbutils.widgets.text("7. Output JSON file", "")
output_file = dbutils.widgets.get("7. Output JSON file")

print("model:", model)
print("dump_all_versions:", dump_all_versions)
print("dump_runs:", dump_runs)
print("dump_permissions:", dump_permissions)
print("show_system_info:", show_system_info)
print("format:", format)
print("output_file:", output_file)

# COMMAND ----------

assert_widget(model, "Missing '1. Model' widget")

# COMMAND ----------

from mlflow_tools.display import dump_model

dct = dump_model.dump(
    model_name = model, 
    dump_all_versions = dump_all_versions,
    dump_runs = dump_runs, 
    dump_permissions = dump_permissions,
    output_file = output_file,
    format = format,
    show_system_info = show_system_info
)

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
