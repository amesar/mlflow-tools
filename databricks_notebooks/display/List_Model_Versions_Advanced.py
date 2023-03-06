# Databricks notebook source
# MAGIC %md ## List Model Versions - Advanced - WIP
# MAGIC 
# MAGIC * Advanced model versions analytics.
# MAGIC * Note that the search is "barebones" and does not yet use search iterators.

# COMMAND ----------

# MAGIC %run ./Common

# COMMAND ----------

from mlflow_tools.display.list_model_versions_advanced import mk_versions_pandas_df 
import mlflow
client = mlflow.client.MlflowClient()
models = client.search_registered_models()

# COMMAND ----------

# MAGIC %md ### Show "latest versions" of models

# COMMAND ----------

pdf = mk_versions_pandas_df(models, get_latest_versions=True)
df = spark.createDataFrame(pdf)
display(df)

# COMMAND ----------

df.createOrReplaceTempView("tbl") 

# COMMAND ----------

# MAGIC %sql select count(*) from tbl where `Run exists` = 'true' ;

# COMMAND ----------

# MAGIC %sql select count(*) from tbl where `Run exists` = 'false' ;

# COMMAND ----------

# MAGIC %md ### Show "all versions" of models

# COMMAND ----------

pdf = mk_versions_pandas_df(models, get_latest_versions=False)
df2 = spark.createDataFrame(pdf)
display(df2)

# COMMAND ----------

df2.createOrReplaceTempView("tbl2")

# COMMAND ----------

# MAGIC %sql select count(*) from tbl2 where `Run exists` = 'false' ;

# COMMAND ----------

# MAGIC %sql select Model, count(*) as run_doesnt_exist from tbl2 
# MAGIC where `Run exists` = 'false' group by Model order by run_doesnt_exist desc