# Databricks notebook source
# MAGIC %md ## Dump a run
# MAGIC
# MAGIC **Overview**
# MAGIC * Shows run info, params, metrics and tags
# MAGIC * Recursively shows all artifacts up to the specified level
# MAGIC
# MAGIC
# MAGIC **Widgets**
# MAGIC * `Run ID`
# MAGIC * `Show tags as dictionary` - show  MLflow tags as a dictionary instead of a list of key/value pairs                  
# MAGIC * `Explode JSON string` - explode JSON attributes which contain a JSON string
# MAGIC * `Artifact max level` - number of artifact levels to show
# MAGIC * `Format` - JSON or YAML
# MAGIC * `Output file` - if set, write output to file

# COMMAND ----------

# MAGIC %run ../Common

# COMMAND ----------

# MAGIC %md ### Widgets

# COMMAND ----------

dbutils.widgets.text("1. Run ID", "")
dbutils.widgets.dropdown("2. Show tags as dictionary","no",["yes","no"])
dbutils.widgets.dropdown("3. Explode JSON string","yes",["yes","no"])
dbutils.widgets.text("4. Artifact max level", "1")
dbutils.widgets.dropdown("5. Format","json",["json","yaml"])
dbutils.widgets.text("6. Output file", "")

run_id = dbutils.widgets.get("1. Run ID")
show_tags_as_dict = dbutils.widgets.get("2. Show tags as dictionary") == "yes"
explode_json_string = dbutils.widgets.get("3. Explode JSON string") == "yes"
artifact_max_level = int(dbutils.widgets.get("4. Artifact max level"))
format = dbutils.widgets.get("5. Format")
output_file = dbutils.widgets.get("6. Output file")

print("run_id:", run_id)
print("show_tags_as_dict:", show_tags_as_dict)
print("explode_json_string:", explode_json_string)
print("artifact_max_level:", artifact_max_level)
print("format:", format)
print("output_file:", output_file)

# COMMAND ----------

assert_widget(run_id, "1. Run ID")

# COMMAND ----------

# MAGIC %md ### Display run details

# COMMAND ----------

from mlflow_tools.display import dump_run

dct = dump_run.dump(
    run_id = run_id, 
    show_tags_as_dict = show_tags_as_dict,
    explode_json_string = explode_json_string,
    artifact_max_level = artifact_max_level, 
    format = format
)

# COMMAND ----------

# MAGIC %md ### Write output to file

# COMMAND ----------

write_file(dct, output_file, format)
