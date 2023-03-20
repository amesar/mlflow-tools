# Databricks notebook source
# MAGIC %md ## Console Shell Scripts
# MAGIC 
# MAGIC Demonstrates how to call "console" command line scripts from shell (%sh).
# MAGIC 
# MAGIC Last updated: 2023-03-19

# COMMAND ----------

# MAGIC %md ### Setup

# COMMAND ----------

# MAGIC %pip install git+https:///github.com/amesar/mlflow-tools/#egg=mlflow-tools

# COMMAND ----------

# MAGIC %md ### Display available console scripts 

# COMMAND ----------

# MAGIC %sh curl https://raw.githubusercontent.com/amesar/mlflow-tools/master/setup.py | tail -n 15

# COMMAND ----------

# MAGIC %md ### Count MLflow objects

# COMMAND ----------

# MAGIC %sh count-objects --help

# COMMAND ----------

# MAGIC %sh count-objects --experiments --models  --versions-by-models

# COMMAND ----------

# MAGIC %md ### List experiments

# COMMAND ----------

# MAGIC %md ##### List experiments - help

# COMMAND ----------

# MAGIC %sh list-experiments --help

# COMMAND ----------

# MAGIC %md ##### List experiments

# COMMAND ----------

# MAGIC %sh list-experiments

# COMMAND ----------

# MAGIC %md ##### List experiments - fewer columns

# COMMAND ----------

# MAGIC %sh list-experiments --verbose False

# COMMAND ----------

# MAGIC %md ##### List experiments - just deleted experiments

# COMMAND ----------

# MAGIC %sh list-experiments --verbose False --view-type deleted_only

# COMMAND ----------

# MAGIC %md ### List registered models

# COMMAND ----------

# MAGIC %sh list-registered-models --help

# COMMAND ----------

# MAGIC %sh list-registered-models

# COMMAND ----------

# MAGIC %md ### List model versions

# COMMAND ----------

# MAGIC %sh list-model-versions --help

# COMMAND ----------

# MAGIC %sh list-model-versions --use-by-models True

# COMMAND ----------

# MAGIC %sh list-model-versions --model andre_02a_Sklearn_Train_Predict

# COMMAND ----------

# MAGIC %md ### List model versions - advanced

# COMMAND ----------

# MAGIC %sh list-model-versions-advanced  --help

# COMMAND ----------

# MAGIC %md ##### Show each model's "latest" versions per stage

# COMMAND ----------

# MAGIC %sh list-model-versions-advanced --model all --view latest

# COMMAND ----------

# MAGIC %md ##### Show all versions of each model

# COMMAND ----------

# MAGIC %sh list-model-versions-advanced --model all --view all
