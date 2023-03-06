# Databricks notebook source
# MAGIC %md ## Count MLflow Objects
# MAGIC 
# MAGIC Displays count for the extent of MLflow searcheable objects.
# MAGIC 
# MAGIC Example:
# MAGIC ```
# MAGIC Object counts for 'iterator' implementation
# MAGIC +--------------------+---------+
# MAGIC | Object             |   Count |
# MAGIC |--------------------+---------|
# MAGIC | experiments        |     624 |
# MAGIC | models             |      38 |
# MAGIC | versions by models |      83 |
# MAGIC +--------------------+---------+
# MAGIC ```

# COMMAND ----------

# MAGIC %run ./Common

# COMMAND ----------

from mlflow_tools.api.api_factory import MLFLOW_API_ITERATOR, MLFLOW_API_SEARCH, DEFAULT_MLFLOW_API

# COMMAND ----------

#dbutils.widgets.removeAll()


# COMMAND ----------

dbutils.widgets.dropdown("1. Experiments","yes",["yes","no"])
experiments = dbutils.widgets.get("1. Experiments") == "yes"
dbutils.widgets.dropdown("2. Registered models","yes",["yes","no"])
models = dbutils.widgets.get("2. Registered models") == "yes"
dbutils.widgets.dropdown("3. Model versions","yes",["yes","no"])
versions = dbutils.widgets.get("3. Model versions") == "yes"
dbutils.widgets.dropdown("4. Model versions by models","yes",["yes","no"])
versions_by_models = dbutils.widgets.get("4. Model versions by models") == "yes"

dbutils.widgets.dropdown("5. Implementation",MLFLOW_API_ITERATOR,[MLFLOW_API_ITERATOR,MLFLOW_API_SEARCH, "both"])
implementation = dbutils.widgets.get("5. Implementation")

print("experiments:", experiments)
print("models:", models)
print("versions:", versions)
print("versions_by_models:", versions_by_models)
print("implementation:", implementation)

# COMMAND ----------



# COMMAND ----------

from mlflow_tools.display import count_objects

count_objects.count(
    mlflow_api=implementation,
    experiments=experiments,
    models=models, 
    versions=versions, 
    versions_by_models=versions_by_models
)