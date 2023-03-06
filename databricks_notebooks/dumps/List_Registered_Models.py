# Databricks notebook source
# MAGIC %md ## List Registered Models

# COMMAND ----------

# MAGIC %run ./Common

# COMMAND ----------

dbutils.widgets.text("CSV file", "")
csv_file = dbutils.widgets.get("CSV file")
csv_file

# COMMAND ----------

from mlflow_tools.tools import list_models
df = list_models.to_pandas_dataframe()
display(df)

# COMMAND ----------

write_csv_file(df, csv_file)