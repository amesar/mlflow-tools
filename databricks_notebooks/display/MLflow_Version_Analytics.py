# Databricks notebook source
# MAGIC %md ## List MLflow Registered Models

# COMMAND ----------

# MAGIC %run ./Common

# COMMAND ----------

from mlflow_tools.api import api_factory
pandas_api = api_factory.get_pandas_api()
pdf = pandas_api.search_registered_models()

df = spark.createDataFrame(pdf)
df.createOrReplaceTempView("models")
display(df)

# COMMAND ----------

pdf = pandas_api.search_model_versions_by_models()
df = spark.createDataFrame(pdf)
df.createOrReplaceTempView("versions")
display(df)

# COMMAND ----------

# MAGIC %sql
# MAGIC select m.name, count(*) as num_versions from models m
# MAGIC left join versions v on v.name = m.name
# MAGIC group by m.name
# MAGIC order by num_versions desc

# COMMAND ----------

# MAGIC %sql
# MAGIC select m.name, v.version, v.current_stage from models m
# MAGIC left join versions v on v.name = m.name
# MAGIC order by m.name, v.current_stage

# COMMAND ----------

# MAGIC %sql
# MAGIC select m.name, v.version, v.current_stage, v.creation_timestamp from models m
# MAGIC left join versions v on v.name = m.name
# MAGIC where m.name like '%andre%'
# MAGIC order by m.name, v.current_stage

# COMMAND ----------

