# Databricks notebook source
# MAGIC %md ## MLflow Display Tools
# MAGIC 
# MAGIC **Overview**
# MAGIC * Notebooks to display results as dataframes from MLflow search API methods.
# MAGIC * Uses wheel from https://github.com/amesar/mlflow-tools 
# MAGIC 
# MAGIC **List Tools**
# MAGIC * [Count_Objects]($Count_Objects) - summary counts of experiments, registered models and model versions,
# MAGIC * [List_Experiments]($List_Experiments)
# MAGIC * [List_Registered_Models]($List_Registered_Models)
# MAGIC * [List_Model_Versions]($List_Model_Versions)
# MAGIC   * [List_Model_Versions_Advanced]($List_Model_Versions_Advanced) - Advanced versions analytics. WIP.
# MAGIC 
# MAGIC **Dump Tools**
# MAGIC * [Dump_Experiment]($Dump_Experiment)
# MAGIC * [Delete_Registered_Model]($Delete_Registered_Model)
# MAGIC 
# MAGIC 
# MAGIC **Other**
# MAGIC * [Common]($Common)
# MAGIC 
# MAGIC **Documentation**
# MAGIC * [MLflow Spark Datasource Example](https://docs.databricks.com/_static/notebooks/mlflow/mlflow-datasource.html) - Databricks documentation.
# MAGIC 
# MAGIC Last updated: 2023-03-05