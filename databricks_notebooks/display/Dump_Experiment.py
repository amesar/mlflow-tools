# Databricks notebook source
# MAGIC %md ## Dump experiment with all its runs
# MAGIC
# MAGIC **Overview**
# MAGIC * Shows run info, params, metrics and tags
# MAGIC * Recursively shows all artifacts up to the specified level
# MAGIC * Note: Makes lots of calls to API to show artifacts info so be aware
# MAGIC
# MAGIC **Widgets**
# MAGIC * `Experiment ID or name` - either the experiment name or the ID
# MAGIC * `Artifact max level` - number of artifact levels to show
# MAGIC * `Dump runs` - dump runs (by default dump only run.info)
# MAGIC * `Dump run data` - dump run data (params, metrics and tags) in addition to run.info if showing runs
# MAGIC * `Dump permissions` - dump run data if showing runs
# MAGIC * `Show tags as dictionary` - show  MLflow tags as a dictionary instead of a list of key/value pairs                  
# MAGIC * `Explode JSON string` - explode JSON attributes which contain a JSON string
# MAGIC * `Format` - JSON or YAML
# MAGIC * `Output file` - if set, write output to file
# MAGIC
# MAGIC **MLflow Spark Data Source**
# MAGIC * Also demonstrates usage of MLflow Spark Data Source `mlflow-experiment`.
# MAGIC * Databricks documentation
# MAGIC   * [MLflow experiment - Load Data](https://docs.databricks.com/external-data/mlflow-experiment.html)
# MAGIC   * [MLflow Spark Datasource Example](https://docs.databricks.com/_static/notebooks/mlflow/mlflow-datasource.html)

# COMMAND ----------

# MAGIC %run ../Common

# COMMAND ----------

# MAGIC %md ### Widgets

# COMMAND ----------

dbutils.widgets.remove("5. Show permissions")

# COMMAND ----------

dbutils.widgets.text("1. Experiment ID or name", "")
dbutils.widgets.text("2. Artifact max level", "1")
dbutils.widgets.dropdown("3. Dump runs", "no", ["yes","no"])
dbutils.widgets.dropdown("4. Dump run data", "no", ["yes","no"])
dbutils.widgets.dropdown("5. Dump permissions", "no", ["yes","no"])
dbutils.widgets.dropdown("6. Show tags as dictionary", "yes", ["yes","no"])
dbutils.widgets.dropdown("7. Explode JSON string", "yes", ["yes","no"])
dbutils.widgets.dropdown("8. Format", "json", ["json","yaml"])
dbutils.widgets.text("9. Output file", "")

experiment_id_or_name = dbutils.widgets.get("1. Experiment ID or name")
artifact_max_level = int(dbutils.widgets.get("2. Artifact max level"))
dump_runs = dbutils.widgets.get("3. Dump runs") == "yes"
dump_run_data = dbutils.widgets.get("4. Dump run data") == "yes"
dump_permissions = dbutils.widgets.get("5. Dump permissions") == "yes"
show_tags_as_dict = dbutils.widgets.get("6. Show tags as dictionary") == "yes"
explode_json_string = dbutils.widgets.get("7. Explode JSON string") == "yes"
format = dbutils.widgets.get("8. Format")
output_file = dbutils.widgets.get("9. Output file")

print("experiment_id_or_name:", experiment_id_or_name)
print("artifact_max_level:", artifact_max_level)
print("dump_runs:", dump_runs)
print("dump_run_data:", dump_run_data)
print("dump_permissions:", dump_permissions)
print("show_tags_as_dict:", show_tags_as_dict)
print("explode_json_string:", explode_json_string)
print("format:", format)
print("output_file:", output_file)

# COMMAND ----------

assert_widget(experiment_id_or_name, "1. Experiment ID or name")

# COMMAND ----------

# MAGIC %md ### Display experiment details

# COMMAND ----------

from mlflow_tools.display import dump_experiment

dct = dump_experiment.dump(
    experiment_id_or_name = experiment_id_or_name, 
    artifact_max_level = artifact_max_level, 
    dump_runs = dump_runs, 
    dump_run_data = dump_run_data, 
    dump_permissions = dump_permissions,
    show_tags_as_dict = show_tags_as_dict,
    explode_json_string = explode_json_string,
    format = format,
    output_file = output_file
)

# COMMAND ----------

# MAGIC %md ### MLflow Spark Datasource
# MAGIC
# MAGIC * See [MLflow Spark Datasource Example](https://docs.databricks.com/_static/notebooks/mlflow/mlflow-datasource.html) documentation.

# COMMAND ----------

if experiment_id_or_name.startswith("/"):
    import mlflow
    client = mlflow.MlflowClient()
    exp = client.get_experiment_by_name(experiment_id_or_name)
    experiment_id = exp.experiment_id
else:
    experiment_id = experiment_id_or_name
df = spark.read.format("mlflow-experiment").load(experiment_id)
display(df)
