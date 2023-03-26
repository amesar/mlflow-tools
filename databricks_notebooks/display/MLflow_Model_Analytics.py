# Databricks notebook source
# MAGIC %md ## MLflow Version Analytics
# MAGIC 
# MAGIC Some queries joining registered models and model version tables.

# COMMAND ----------

# MAGIC %md #### Setup

# COMMAND ----------

# MAGIC %run ../Common

# COMMAND ----------

# MAGIC %md #### Create registered models table

# COMMAND ----------

from mlflow_tools.api import api_factory
pandas_api = api_factory.get_pandas_api()
pdf = pandas_api.search_registered_models()

df = spark.createDataFrame(pdf)
df.createOrReplaceTempView("models")
display(df)

# COMMAND ----------

# MAGIC %md #### Create model versions table

# COMMAND ----------

pdf = pandas_api.search_model_versions_by_models()
df = spark.createDataFrame(pdf)
df.createOrReplaceTempView("versions")
display(df)

# COMMAND ----------

# MAGIC %md #### Get versions count per model

# COMMAND ----------

# MAGIC %sql
# MAGIC select m.name, count(*) as num_versions from models m
# MAGIC left join versions v on v.name = m.name
# MAGIC group by m.name
# MAGIC order by num_versions desc

# COMMAND ----------

# MAGIC %md #### Show versions of each model

# COMMAND ----------

# MAGIC %sql
# MAGIC select m.name, v.version, v.current_stage from models m
# MAGIC left join versions v on v.name = m.name
# MAGIC order by m.name, v.current_stage

# COMMAND ----------

# MAGIC %md #### Show versions of each model by name filter

# COMMAND ----------

# MAGIC %sql
# MAGIC select m.name, v.version, v.current_stage, v.creation_timestamp from models m
# MAGIC left join versions v on v.name = m.name
# MAGIC where m.name like '%andre%'
# MAGIC order by m.name, v.current_stage

# COMMAND ----------

# MAGIC %sql
# MAGIC select v.name, v.* from models m
# MAGIC left join versions v on v.name = m.name
# MAGIC where m.name like '%andre%'
# MAGIC order by m.name, v.current_stage
