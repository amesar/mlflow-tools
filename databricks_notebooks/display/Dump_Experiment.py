# Databricks notebook source
# MAGIC %md ## Dump experiment with all its runs
# MAGIC 
# MAGIC **Overview**
# MAGIC * Shows run info, params, metrics and tags
# MAGIC * Recursively shows all artifacts up to the specified level
# MAGIC * Note: Makes lots of calls to API to show artifacts info so be aware
# MAGIC 
# MAGIC **Widgets**
# MAGIC * Experiment ID or name - Either the experiment name or the ID
# MAGIC * Artifact max level - number of artifact levels to show
# MAGIC * Show runs - Show runs
# MAGIC * Show run data - Show run data if showing runs
# MAGIC * Format - JSON or YAML
# MAGIC * Output file - if set, write output to file
# MAGIC 
# MAGIC **MLflow Spark Data Source documentation**
# MAGIC * [MLflow experiment - Load Data](https://docs.databricks.com/external-data/mlflow-experiment.html)
# MAGIC * [MLflow Spark Datasource Example](https://docs.databricks.com/_static/notebooks/mlflow/mlflow-datasource.html)

# COMMAND ----------

# MAGIC %run ./Common

# COMMAND ----------

# MAGIC %md ### Widgets

# COMMAND ----------

dbutils.widgets.text("1. Experiment ID or name", "")
dbutils.widgets.text("2. Artifact max level", "1")
dbutils.widgets.dropdown("3. Show runs","no",["yes","no"])
dbutils.widgets.dropdown("4. Show run data","no",["yes","no"])

dbutils.widgets.dropdown("5. Format","json",["json","yaml"])
dbutils.widgets.text("6. Output file", "")

experiment_id_or_name = dbutils.widgets.get("1. Experiment ID or name")
artifact_max_level = int(dbutils.widgets.get("2. Artifact max level"))
show_runs = dbutils.widgets.get("3. Show runs") == "yes"
show_run_data = dbutils.widgets.get("4. Show run data") == "yes"
format = dbutils.widgets.get("5. Format")
output_file = dbutils.widgets.get("6. Output file")

if experiment_id_or_name=="":
    raise Exception("Missing '1. Experiment ID or name' value")
print("experiment_id_or_name:",experiment_id_or_name)
print("artifact_max_level:",artifact_max_level)
print("show_runs:",show_runs)
print("show_run_data:",show_run_data)
print("format:",format)
print("output_file:",output_file)

# COMMAND ----------

# MAGIC %md ### Display experiment details

# COMMAND ----------

from mlflow_tools.display import dump_experiment

dct = dump_experiment.dump(experiment_id_or_name, 
                     artifact_max_level, 
                     show_runs=show_runs, 
                     show_run_data=show_run_data, 
                     format=format,
                     explode_json_string=False)

# COMMAND ----------

# MAGIC %md ### Write output to file

# COMMAND ----------

write_file(dct, output_file, format)

# COMMAND ----------

# MAGIC %md ### MLflow Spark Datasource
# MAGIC 
# MAGIC * See [MLflow Spark Datasource Example](https://docs.databricks.com/_static/notebooks/mlflow/mlflow-datasource.html) documentation.

# COMMAND ----------

if experiment_id_or_name.startswith("/"):
    import mlflow
    client = mlflow.client.MlflowClient()
    exp = client.get_experiment_by_name(experiment_id_or_name)
    experiment_id = exp.experiment_id
else:
    experiment_id = experiment_id_or_name
df = spark.read.format("mlflow-experiment").load(experiment_id)
display(df)