# Databricks notebook source
# MAGIC %md ### Dump registered model details
# MAGIC 
# MAGIC Overview
# MAGIC * Dump registered in JSON or YAML
# MAGIC 
# MAGIC Widgets
# MAGIC * Model - registered model name
# MAGIC * Show version runs - show details of the version runs
# MAGIC * Output CSV file - JSON or YAML

# COMMAND ----------

# MAGIC %run ./Common

# COMMAND ----------

dbutils.widgets.remove("4. Output file")
dbutils.widgets.text("1. Model", "")
model = dbutils.widgets.get("1. Model")
dbutils.widgets.dropdown("2. Show version runs", "yes", ["yes","no"])
show_runs = dbutils.widgets.get("2. Show version runs") == "yes"
dbutils.widgets.dropdown("3. Format","json", ["json", "yaml"])
format = dbutils.widgets.get("3. Format")
dbutils.widgets.text("4. Output JSON file", "")
output_file = dbutils.widgets.get("4. Output JSON file")

assert_widget(model, "Missing '1. Model' widget")
 
print("model:", model)
print("show_runs:", show_runs)
print("format:", format)
print("output_file:", output_file)

# COMMAND ----------

from mlflow_tools.tools import dump_model

dct = dump_model.dump(model, 
                      show_runs=show_runs, 
                      format=format, 
                      format_datetime=True)

# COMMAND ----------

write_file(dct, output_file, format)