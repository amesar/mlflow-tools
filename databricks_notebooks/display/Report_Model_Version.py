# Databricks notebook source
# MAGIC %md ### Report model version
# MAGIC
# MAGIC Overview
# MAGIC * Display model governance report for model version
# MAGIC
# MAGIC Widgets
# MAGIC * `1. Model name` - registered model name
# MAGIC * `2. Version` - model version
# MAGIC * `3. Format` - JSON or YAML
# MAGIC * `4. Output file`

# COMMAND ----------

# MAGIC %run ../Common

# COMMAND ----------

#dbutils.widgets.removeAll()

# COMMAND ----------

# Sklearn_Wine_ONNX_ws

# COMMAND ----------

dbutils.widgets.text("1. Registered model", "")
model_name = dbutils.widgets.get("1. Registered model")

dbutils.widgets.text("2. Version", "")
version = dbutils.widgets.get("2. Version")

dbutils.widgets.dropdown("3. Format","json", ["json", "yaml"])
format = dbutils.widgets.get("3. Format")

dbutils.widgets.text("4. Output JSON file", "")
output_file = dbutils.widgets.get("4. Output JSON file")

print("model_name:", model_name)
print("version:", version)
print("format:", format)
print("output_file:", output_file)

# COMMAND ----------

assert_widget(model_name, "Missing '01. Registered model'")
assert_widget(version, "Missing '02. Version'")

# COMMAND ----------

report_model_version.report(
    model_name = model_name, 
    version = version,
    format = format,
    output_file = output_file
)
