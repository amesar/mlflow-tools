# Databricks notebook source
# MAGIC %md ## mlflow-tools - Display Notebooks
# MAGIC
# MAGIC **Overview**
# MAGIC * Notebooks to display individual or lists of MLflow objects.
# MAGIC * Plus some analytics about models and versions.
# MAGIC * Github: https://github.com/amesar/mlflow-tools/tree/master/databricks_notebooks/display. 
# MAGIC
# MAGIC **List tools**
# MAGIC * Display results as dataframes from MLflow search API methods.
# MAGIC * [Count_Objects]($Count_Objects) - summary counts of experiments, registered models and model versions.
# MAGIC * [List_Experiments]($List_Experiments)
# MAGIC * [List_Registered_Models]($List_Registered_Models)
# MAGIC * [List_Model_Versions]($List_Model_Versions)
# MAGIC   * [List_Model_Versions_With_Runs]($List_Model_Versions_With_Runs) - display information on model versions and their runs.
# MAGIC   * [MLflow_Model_Analytics]($MLflow_Model_Analytics) - queries on joining models and versions.
# MAGIC
# MAGIC **Dump tools**
# MAGIC * [Dump_Registered_Model]($Dump_Registered_Model)
# MAGIC * [Dump_Model_Version]($Dump_Model_Version)
# MAGIC * [Dump_Experiment]($Dump_Experiment)
# MAGIC   * Also demonstrates usage of [Databricks mlflow-experiment Spark Data Source](https://docs.databricks.com/_static/notebooks/mlflow/mlflow-datasource.html).
# MAGIC * [Dump_Run]($Dump_Run)
# MAGIC * [Dump_MLflow_Model]($Dump_MLflow_Model) - Dump MLflow ModelInfo for a model URI
# MAGIC
# MAGIC **MLflow model tools**
# MAGIC * [Report_Model_Version]($Report_Model_Version) - Model governance report for model version and its underlying MLflow model
# MAGIC * [Download_MLflow_Model]($Download_MLflow_Model) - Download  MLflow model by model URI as in `models:/my-model/production`
# MAGIC
# MAGIC **Databricks MLflow Spark Datasource**
# MAGIC * [MLflow Spark Datasource Example](https://docs.databricks.com/_static/notebooks/mlflow/mlflow-datasource.html) - Databricks notebook example.
# MAGIC
# MAGIC **Other**
# MAGIC * [../Common]($../Common)
# MAGIC
# MAGIC **NOTE**
# MAGIC
# MAGIC * Requires Databricks Runtime 13 or 12.2.
# MAGIC
# MAGIC Last updated: _2023-06-11_
