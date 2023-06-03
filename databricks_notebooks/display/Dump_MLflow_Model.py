# Databricks notebook source
# MAGIC %md ### Dump MLflow model - ModelInfo
# MAGIC
# MAGIC Overview
# MAGIC * Dump MLflow model
# MAGIC
# MAGIC Widgets
# MAGIC * `1. Model URI` 
# MAGIC * `2. Show signature details` - TODO
# MAGIC * `3. Dump run` - version's run
# MAGIC * `4. Dump experiment` - run'experiment
# MAGIC * `5. Format` - JSON or YAML
# MAGIC * `6. Output file`

# COMMAND ----------

# MAGIC %run ../Common

# COMMAND ----------

dbutils.widgets.text("1. Model URI", "")
model_uri = dbutils.widgets.get("1. Model URI")

dbutils.widgets.dropdown("2. Show signature details", "no", ["yes","no"])
signature_details = dbutils.widgets.get("2. Show signature details") == "yes"

dbutils.widgets.dropdown("3. Dump run", "no", ["yes","no"])
dump_run = dbutils.widgets.get("3. Dump run") == "yes"

dbutils.widgets.dropdown("4. Dump experiment", "no", ["yes","no"])
dump_experiment = dbutils.widgets.get("4. Dump experiment") == "yes"

dbutils.widgets.dropdown("5. Format","json", ["json", "yaml"])
format = dbutils.widgets.get("5. Format")

dbutils.widgets.text("6. Output file", "")
output_file = dbutils.widgets.get("6. Output file")

print("model_uri:", model_uri)
print("signature_details:", signature_details)
print("dump_run:", dump_run)
print("dump_experiment:", dump_experiment)
print("format:", format)
print("output_file:", output_file)

# COMMAND ----------

assert_widget(model_uri, "Missing '1. Model URI'")

# COMMAND ----------

from mlflow_tools.display import dump_mlflow_model

dump_mlflow_model.dump(
    model_uri = model_uri, 
    dump_run = dump_run,
    dump_experiment = dump_experiment,
    output_file = output_file
)
