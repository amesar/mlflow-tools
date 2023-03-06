# Databricks notebook source
# MAGIC %md ## List MLflow Experiments

# COMMAND ----------

# MAGIC %run ./Common

# COMMAND ----------

from mlflow_tools.api import api_factory
pandas_api = api_factory.get_pandas_api()

pdf = pandas_api.search_experiments()
df = spark.createDataFrame(pdf)
display(df)