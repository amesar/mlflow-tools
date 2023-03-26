# Databricks notebook source
# MAGIC %md ### Rename registered model
# MAGIC 
# MAGIC Widgets
# MAGIC * `1. Model` - model to be renamed
# MAGIC * `2. New model` - new model name
# MAGIC * `3.` Fudge version stage - "fudge" version stage: Transition stage to 'Archived' before delete, and then restore original version stage for new model

# COMMAND ----------

# MAGIC %run ../Common

# COMMAND ----------

dbutils.widgets.text("1. Model", "")
model_name = dbutils.widgets.get("1. Model")

dbutils.widgets.text("2. New model", "")
new_model_name = dbutils.widgets.get("2. New model")

dbutils.widgets.dropdown("3. Fudge version stage", "yes", ["yes","no"])
fudge_version_stage = dbutils.widgets.get("3. Fudge version stage") == "yes"
 
print("model_name:", model_name)
print("new_model_name:", new_model_name)
print("fudge_version_stage:", fudge_version_stage)

# COMMAND ----------

assert_widget(model_name, "Missing '1. Model' widget")
assert_widget(new_model_name, "Missing '2. New model' widget")

# COMMAND ----------

from mlflow_tools.tools.rename_model import rename_model

rename_model(
    model_name = model_name,
    new_model_name = new_model_name,
    fudge_version_stage = fudge_version_stage
)
