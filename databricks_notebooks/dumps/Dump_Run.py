# Databricks notebook source
# MAGIC %md ### Dump run details
# MAGIC 
# MAGIC Overvew
# MAGIC * Output format is JSON, YAML or text
# MAGIC * Shows params, metrics and tags
# MAGIC * Recursively shows all artifacts up to the specified level
# MAGIC * Note: Makes lots of calls to API, so beware of runs with many artifacts
# MAGIC * Uses: https://github.com/amesar/mlflow-tools/blob/master/mlflow_tools/tools/dump_run.py
# MAGIC 
# MAGIC Widgets
# MAGIC * Run ID
# MAGIC * Artifact max level - number of levels to display
# MAGIC * Format - JSON or YAML

# COMMAND ----------

# MAGIC %run ./Common

# COMMAND ----------

dbutils.widgets.text("1. Run ID", "")
run_id = dbutils.widgets.get("1. Run ID")

dbutils.widgets.text("2. Artifact Max Level", "1")
artifact_max_level = int(dbutils.widgets.get("2. Artifact Max Level"))

dbutils.widgets.dropdown("3. Format","json",["json","yaml"])
format = dbutils.widgets.get("3. Format")

dbutils.widgets.dropdown("4. Explode JSON strings","no",["yes","no"])
explode_json_string = dbutils.widgets.get("4. Explode JSON strings") == "yes"

dbutils.widgets.text("5. Output file", "")
output_file = dbutils.widgets.get("5. Output file")

print("run_id:",run_id)
print("artifact_max_level:",artifact_max_level)
print("format:",format)
print("explode_json_string:",explode_json_string)
print("output_file:",output_file)

# COMMAND ----------

from mlflow_tools.tools.dump_run import dump_run_id
dct = dump_run_id(run_id, 
                  artifact_max_level=artifact_max_level, 
                  format=format,
                  explode_json_string=explode_json_string)

# COMMAND ----------

write_file(dct, output_file, format)

# COMMAND ----------

import mlflow 
client = mlflow.client.MlflowClient()
run = client.get_run(run_id)
exp = client.get_experiment(run.info.experiment_id)
host_name = dbutils.notebook.entry_point.getDbutils().notebook().getContext().tags().get("browserHostName").get()
uri = f"https://{host_name}/#mlflow/experiments/{exp.experiment_id}/runs/{run_id}"
displayHTML("""<b>Run URI:</b> <a href="{}">{}</a>""".format(uri,uri))