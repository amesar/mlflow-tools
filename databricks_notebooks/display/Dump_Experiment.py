# Databricks notebook source
# MAGIC %md ## Dump experiment with all its runs
# MAGIC
# MAGIC **Overview**
# MAGIC * Shows experiment details and optionally its runs:
# MAGIC   * Shows run info, params, metrics and tags
# MAGIC   * Recursively shows all run artifacts up to the specified level
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
# MAGIC * `Dump raw JSON` - dump JSON as received from API request
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

dbutils.widgets.text("01. Experiment ID or name", "")
dbutils.widgets.text("02. Artifact max level", "1")
dbutils.widgets.dropdown("03. Dump runs", "no", ["yes","no"])
dbutils.widgets.dropdown("04. Dump run data", "no", ["yes","no"])
dbutils.widgets.dropdown("05. Dump permissions", "no", ["yes","no"])
dbutils.widgets.dropdown("06. Show tags as dictionary", "yes", ["yes","no"])
dbutils.widgets.dropdown("07. Explode JSON string", "yes", ["yes","no"])
dbutils.widgets.dropdown("08. Format", "json", ["json","yaml"])
dbutils.widgets.text("09. Output file", "")
dbutils.widgets.dropdown("10. Dump raw JSON", "no", ["yes","no"])

experiment_id_or_name = dbutils.widgets.get("01. Experiment ID or name")
artifact_max_level = int(dbutils.widgets.get("02. Artifact max level"))
dump_runs = dbutils.widgets.get("03. Dump runs") == "yes"
dump_run_data = dbutils.widgets.get("04. Dump run data") == "yes"
dump_permissions = dbutils.widgets.get("05. Dump permissions") == "yes"
show_tags_as_dict = dbutils.widgets.get("06. Show tags as dictionary") == "yes"
explode_json_string = dbutils.widgets.get("07. Explode JSON string") == "yes"
format = dbutils.widgets.get("08. Format")
output_file = dbutils.widgets.get("09. Output file")
dump_raw = dbutils.widgets.get("10. Dump raw JSON") == "yes"

print("experiment_id_or_name:", experiment_id_or_name)
print("artifact_max_level:", artifact_max_level)
print("dump_runs:", dump_runs)
print("dump_run_data:", dump_run_data)
print("dump_permissions:", dump_permissions)
print("show_tags_as_dict:", show_tags_as_dict)
print("explode_json_string:", explode_json_string)
print("format:", format)
print("output_file:", output_file)
print("dump_raw:", dump_raw)

# COMMAND ----------

assert_widget(experiment_id_or_name, "01. Experiment ID or name")

# COMMAND ----------

# MAGIC %md ### Display experiment details

# COMMAND ----------

from mlflow_tools.display import dump_experiment

dct = dump_experiment.dump(
    experiment_id_or_name = experiment_id_or_name, 
    dump_raw = dump_raw,
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
