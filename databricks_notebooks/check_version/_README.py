# Databricks notebook source
# MAGIC %md ## mlflow-tools - Model Version Validation
# MAGIC 
# MAGIC **Overview**
# MAGIC * [Compare_Model_Versions]($Compare_Model_Versions) - Compare two model versions. Check that the cached registry models match and the run models are the same.
# MAGIC * [Check_Model_Version]($Check_Model_Version) - Checks that a model version's run model artifact matches the cached model registry model.
# MAGIC * Full details: https://github.com/amesar/mlflow-tools/blob/master/README_check_version.md
# MAGIC 
# MAGIC **Model Version MLflow Model Diagram**
# MAGIC <br/><br/>
# MAGIC <img src="https://github.com/amesar/mlflow-tools/blob/master/docs/MLflow_Model_Version.png?raw=true" width="700" />
# MAGIC <br/><br/>
# MAGIC 
# MAGIC Last updated: 2023-04-26
