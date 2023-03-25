# Databricks notebook source
# MAGIC %md ## List Model Versions
# MAGIC 
# MAGIC Note: https://github.com/mlflow/mlflow/issues/7967 - search_model_versions() erroneously (per doc) requires a model name 

# COMMAND ----------

# MAGIC %run ./Common

# COMMAND ----------

dbutils.widgets.text("1. Registered model", "")
model_name = dbutils.widgets.get("1. Registered model")
model_name = model_name or None
print("model_name:", model_name)

# COMMAND ----------

#assert_widget(model_name, "1. Registered model") # OSS Mlflow search_model_versions does not require filter whereas Databricks version does

# COMMAND ----------

from mlflow_tools.display.list_model_versions import to_pandas_dataframe
pdf = to_pandas_dataframe(model_name=model_name)
df = spark.createDataFrame(pdf)
display(df)
