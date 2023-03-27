# Databricks notebook source
# MAGIC %md ## Console Shell Scripts
# MAGIC 
# MAGIC Shows how to call console command line scripts from a notebooks shell (%sh) cell. 
# MAGIC 
# MAGIC See https://github.com/amesar/mlflow-tools/tree/master/mlflow_tools/display#mlflow-display-tools.

# COMMAND ----------

# MAGIC %md #### Setup

# COMMAND ----------

dbutils.widgets.text("1. Secrets scope", "")
secrets_scope = dbutils.widgets.get("1. Secrets scope")
dbutils.widgets.text("2. Secrets PAT key", "")
secrets_token_key = dbutils.widgets.get("2. Secrets PAT key")
secrets_scope, secrets_token_key

# COMMAND ----------

# MAGIC %run ./Common

# COMMAND ----------

# MAGIC %md #### Display available console scripts 

# COMMAND ----------

# MAGIC %sh curl https://raw.githubusercontent.com/amesar/mlflow-tools/master/setup.py | tail -n 15

# COMMAND ----------

# MAGIC %md ### Display scripts

# COMMAND ----------

# MAGIC %md #### Count MLflow objects

# COMMAND ----------

# MAGIC %sh count-objects --help

# COMMAND ----------

# MAGIC %sh count-objects --experiments --models  --versions-by-models

# COMMAND ----------

# MAGIC %md #### List experiments

# COMMAND ----------

# MAGIC %md ###### List experiments - help

# COMMAND ----------

# MAGIC %sh list-experiments --help

# COMMAND ----------

# MAGIC %md ###### List experiments

# COMMAND ----------

# MAGIC %sh list-experiments

# COMMAND ----------

# MAGIC %md ###### List experiments - choose your columns

# COMMAND ----------

# MAGIC %sh list-experiments --columns experiment_id,name,creation_time,last_update_time,lifecycle_stage

# COMMAND ----------

# MAGIC %md ###### List experiments - just deleted experiments

# COMMAND ----------

# MAGIC %sh list-experiments \
# MAGIC   --view-type deleted_only \
# MAGIC   --columns=experiment_id,lifecycle_stage

# COMMAND ----------

# MAGIC %md #### List registered models

# COMMAND ----------

# MAGIC %sh list-registered-models --help

# COMMAND ----------

# MAGIC %sh list-registered-models

# COMMAND ----------

# MAGIC %sh list-registered-models \
# MAGIC   --columns name,latest_versions,last_updated_timestamp \
# MAGIC   --sort-attr latest_versions \
# MAGIC   --sort-order desc

# COMMAND ----------

# MAGIC %md #### List model versions

# COMMAND ----------

# MAGIC %sh list-model-versions --help

# COMMAND ----------

# MAGIC %sh list-model-versions --use-by-models True

# COMMAND ----------

# MAGIC %sh list-model-versions --model andre_02a_Sklearn_Train_Predict

# COMMAND ----------

# MAGIC %md #### List model versions with runs

# COMMAND ----------

# MAGIC %sh list-model-versions-with-runs --help

# COMMAND ----------

# MAGIC %sh list-model-versions-with-runs \
# MAGIC   --get-latest-versions True \
# MAGIC   --filter "name like 'andre_%'" 

# COMMAND ----------

# MAGIC %sh list-model-versions-with-runs \
# MAGIC   --get-latest-versions False \
# MAGIC   --model-names all \
# MAGIC   --run-lifecycle-stage deleted

# COMMAND ----------

# MAGIC %sh list-model-versions-with-runs \
# MAGIC   --get-latest-versions False \
# MAGIC   --model-names all

# COMMAND ----------

# MAGIC %md ### Tools scripts

# COMMAND ----------

# MAGIC %sh python -m mlflow_tools.tools.delete_model --help

# COMMAND ----------

# MAGIC %sh python -m mlflow_tools.tools.rename_model --help

# COMMAND ----------

# MAGIC %sh python -m mlflow_tools.tools.download_model --help

# COMMAND ----------

# MAGIC %sh python -m mlflow_tools.tools.find_artifacts --help

# COMMAND ----------

# MAGIC %sh python -m mlflow_tools.tools.best_run  --help

# COMMAND ----------

# MAGIC %sh python -m mlflow_tools.tools.call_model_server --help
