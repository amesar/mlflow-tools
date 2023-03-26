# Databricks notebook source
# MAGIC %md ### Delete registered model and its versions
# MAGIC 
# MAGIC Widgets
# MAGIC * `1. Model` - registered model name
# MAGIC * `2. Delete only versions and not the mode` - Delete only versions and not the mode

# COMMAND ----------

# MAGIC %run ../Common

# COMMAND ----------

dbutils.widgets.text("1. Model", "")
model_name = dbutils.widgets.get("1. Model")

dbutils.widgets.dropdown("2. Delete only versions and not the model", "no", ["yes","no"])
delete_only_versions = dbutils.widgets.get("2. Delete only versions and not the model") == "yes"
 
print("model_name:", model_name)
print("delete_only_versions:", delete_only_versions)

# COMMAND ----------

assert_widget(model, "Missing '1. Model' widget")

# COMMAND ----------

from mlflow_tools.tools.delete_model import delete_model

delete_model(
    model_name = model_name,
    delete_only_versions = delete_only_versions
)
