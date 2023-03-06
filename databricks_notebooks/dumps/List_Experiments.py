# Databricks notebook source
# MAGIC %md ## List MLflow Experiments
# MAGIC 
# MAGIC Widgets:
# MAGIC * CSV file - optionally write output to file
# MAGIC * Verbose - short or long column version

# COMMAND ----------

# MAGIC %run ./Common

# COMMAND ----------

dbutils.widgets.text("CSV file", "")
csv_file = dbutils.widgets.get("CSV file")

dbutils.widgets.dropdown("Verbose","yes",["yes","no"])
verbose = dbutils.widgets.get("Verbose") == "yes"

csv_file, verbose 

# COMMAND ----------

from mlflow_tools.tools import list_experiments
df = list_experiments.to_pandas_dataframe(verbose=verbose)
display(df)

# COMMAND ----------

write_csv_file(df, csv_file)