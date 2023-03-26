# Databricks notebook source
# MAGIC %md ## mlflow-tools - Display Notebooks
# MAGIC 
# MAGIC **Overview**
# MAGIC * Notebooks to display individual or lists of MLflow objects plus some analytics about models and versions.
# MAGIC * pip install repo: https://github.com/amesar/mlflow-tools. See [Common]($Common) notebook.
# MAGIC * Notebook code: https://github.com/amesar/mlflow-tools/tree/master/databricks_notebooks/display. 
# MAGIC 
# MAGIC **Console scripts**
# MAGIC * Shows how to call "console" command line scripts from shell (%sh). Alternative to the List and Dump notebooks.
# MAGIC * [Console_Shell_Scripts]($Console_Shell_Scripts)
# MAGIC 
# MAGIC **List tools**
# MAGIC * Display results as dataframes from MLflow search API methods.
# MAGIC * [Count_Objects]($Count_Objects) - summary counts of experiments, registered models and model versions.
# MAGIC * [List_Experiments]($List_Experiments)
# MAGIC * [List_Registered_Models]($List_Registered_Models)
# MAGIC * [List_Model_Versions]($List_Model_Versions)
# MAGIC   * [List_Model_Versions_With_Runs]($List_Model_Versions_With_Runs) - display information on model versions and their runs.
# MAGIC   * [MLflow_Model_Analytics]($MLflow_Model_Analytics) - queries on joining models and versions.
# MAGIC * [List_Runs]($List_Runs) - TODO
# MAGIC 
# MAGIC **Dump tools**
# MAGIC * [Dump_Registered_Model]($Dump_Registered_Model)
# MAGIC * [Dump_Experiment]($Dump_Experiment)
# MAGIC * [Dump_Run]($Dump_Run)
# MAGIC 
# MAGIC **Other**
# MAGIC * [Common]($Common)
# MAGIC 
# MAGIC **Documentation**
# MAGIC * [MLflow Spark Datasource Example](https://docs.databricks.com/_static/notebooks/mlflow/mlflow-datasource.html) - Databricks documentation.
# MAGIC 
# MAGIC Last updated: 2023-03-26
