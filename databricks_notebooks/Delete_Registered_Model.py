# Databricks notebook source
# MAGIC %md ### Delete registered model and its versions

# COMMAND ----------

# MAGIC %run ./Common

# COMMAND ----------

dbutils.widgets.removeAll()

dbutils.widgets.text("1. Registered model", "")
model = dbutils.widgets.get("1. Registered model")

dbutils.widgets.dropdown("2. Delete only versions","no",["yes","no"])
delete_only_versions = dbutils.widgets.get("2. Delete only versions") == "yes"

print("model:", model)
print("delete_only_versions:", delete_only_versions)

assert_widget(model, "1. Registered model")

# COMMAND ----------

from mlflow_tools.tools.delete_model import delete_model

delete_model(model, delete_only_versions)