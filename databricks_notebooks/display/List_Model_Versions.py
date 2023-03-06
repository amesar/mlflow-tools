# Databricks notebook source
# MAGIC %md ## List Model Versions

# COMMAND ----------

# MAGIC %run ./Common

# COMMAND ----------

dbutils.widgets.text("1. Registered model", "")
model_name = dbutils.widgets.get("1. Registered model")
model_name = model_name or None
print("model_name:",model_name)

# COMMAND ----------

from mlflow_tools.display.list_model_versions import to_pandas_dataframe
pdf = to_pandas_dataframe(model_name=model_name)
df = spark.createDataFrame(pdf)
display(df)