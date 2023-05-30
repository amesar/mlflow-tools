# Databricks notebook source
# MAGIC %md ### Dump model version details
# MAGIC
# MAGIC Overview
# MAGIC * Dump registered model version as JSON or YAML
# MAGIC
# MAGIC Widgets
# MAGIC * `1. Model name` - registered model name
# MAGIC * `2. Version` - model version
# MAGIC * `3. Dump run` - version's run
# MAGIC * `4. Dump experiment` - run'experiment
# MAGIC * `5. Dump registered model` - version's registered model 
# MAGIC * `6. Dump permissions` - dump run data if showing runs
# MAGIC * `5. Format` - JSON or YAML
# MAGIC * `6. Output file`

# COMMAND ----------

# MAGIC %run ../Common

# COMMAND ----------

dbutils.widgets.text("01. Registered model", "")
model_name = dbutils.widgets.get("01. Registered model")

dbutils.widgets.text("02. Version", "")
version = dbutils.widgets.get("02. Version")

dbutils.widgets.dropdown("03. Dump run", "no", ["yes","no"])
dump_run = dbutils.widgets.get("03. Dump run") == "yes"

dbutils.widgets.dropdown("04. Dump experiment", "no", ["yes","no"])
dump_experiment = dbutils.widgets.get("04. Dump experiment") == "yes"

dbutils.widgets.dropdown("05. Dump registered model", "no", ["yes","no"])
dump_registered_model = dbutils.widgets.get("05. Dump registered model") == "yes"

dbutils.widgets.dropdown("06. Dump permissions", "no", ["yes","no"])
dump_permissions = dbutils.widgets.get("06. Dump permissions") == "yes"

dbutils.widgets.dropdown("07. Format","json", ["json", "yaml"])
format = dbutils.widgets.get("07. Format")

dbutils.widgets.text("08. Output JSON file", "")
output_file = dbutils.widgets.get("08. Output JSON file")

print("model_name:", model_name)
print("version:", version)
print("dump_run:", dump_run)
print("dump_experiment:", dump_experiment)
print("dump_registered_model:", dump_registered_model)
print("dump_permissions:", dump_permissions)
print("format:", format)
print("output_file:", output_file)

# COMMAND ----------

assert_widget(model_name, "Missing '01. Registered model'")
assert_widget(version, "Missing '02. Version'")

# COMMAND ----------

from mlflow_tools.display import dump_model_version

dct = dump_model_version.dump(
    model_name = model_name, 
    version = version,
    dump_run = dump_run,
    dump_experiment = dump_experiment,
    dump_registered_model = dump_registered_model,
    dump_permissions = dump_permissions,
    format = format,
    output_file = output_file
)

# COMMAND ----------

from mlflow_tools.display.list_model_versions import to_pandas_dataframe 
pdf = to_pandas_dataframe(model)
df = spark.createDataFrame(pdf)
display(df)
