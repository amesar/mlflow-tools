# Databricks notebook source
# MAGIC %md ## Set Model Alias

# COMMAND ----------

# MAGIC %run ../Common

# COMMAND ----------

dbutils.widgets.text("1. Model", "")
model_name = dbutils.widgets.get("1. Model")

dbutils.widgets.text("2. Version", "")
model_version = dbutils.widgets.get("2. Version")

dbutils.widgets.text("3. Alias", "")
alias = dbutils.widgets.get("3. Alias")

print("model_name:", model_name)
print("model_version:", model_version)
print("alias:", alias)

# COMMAND ----------

assert_widget(model_name, "Missing '1. Model")
assert_widget(model_version, "Missing '2. Version")
assert_widget(alias, "Missing '3. Alias")

# COMMAND ----------

import mlflow
mlflow.set_registry_uri("databricks-uc")
client = mlflow.MlflowClient()

# COMMAND ----------

model = client.get_registered_model(model_name)
model.aliases

# COMMAND ----------

client.set_registered_model_alias(model_name, alias, model_version)

# COMMAND ----------

model = client.get_registered_model(model_name)
model.aliases
