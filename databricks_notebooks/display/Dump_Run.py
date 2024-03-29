# Databricks notebook source
# MAGIC %md ## Dump a run
# MAGIC
# MAGIC **Overview**
# MAGIC * Shows run info, params, metrics and tags
# MAGIC * Recursively shows all artifacts up to the specified level
# MAGIC
# MAGIC
# MAGIC **Widgets**
# MAGIC * `1. Run ID`
# MAGIC * `2. Artifact max level` - number of artifact levels to show
# MAGIC * `3. Show tags as dictionary` - show  MLflow tags as a dictionary instead of a list of key/value pairs                  
# MAGIC * `4. Explode JSON string` - explode JSON attributes which contain a JSON string
# MAGIC * `5. Format` - JSON or YAML
# MAGIC * `6. Output file` - if set, write output to file
# MAGIC * `7. Dump raw JSON` - dump JSON as received from API request

# COMMAND ----------

# MAGIC %run ../Common

# COMMAND ----------

# MAGIC %md ### Widgets

# COMMAND ----------

dbutils.widgets.text("1. Run ID", "")
dbutils.widgets.text("2. Artifact max level", "1")
dbutils.widgets.dropdown("3. Show tags as dictionary", "yes", ["yes","no"])
dbutils.widgets.dropdown("4. Explode JSON string", "yes", ["yes","no"])
dbutils.widgets.dropdown("5. Format", "json", ["json","yaml"])
dbutils.widgets.text("6. Output file", "")
dbutils.widgets.dropdown("7. Dump raw JSON", "no", ["yes","no"])

run_id = dbutils.widgets.get("1. Run ID")
artifact_max_level = int(dbutils.widgets.get("2. Artifact max level"))
show_tags_as_dict = dbutils.widgets.get("3. Show tags as dictionary") == "yes"
explode_json_string = dbutils.widgets.get("4. Explode JSON string") == "yes"
format = dbutils.widgets.get("5. Format")
output_file = dbutils.widgets.get("6. Output file")
dump_raw = dbutils.widgets.get("7. Dump raw JSON") == "yes"

print("run_id:", run_id)
print("artifact_max_level:", artifact_max_level)
print("show_tags_as_dict:", show_tags_as_dict)
print("explode_json_string:", explode_json_string)
print("format:", format)
print("output_file:", output_file)
print("dump_raw:", dump_raw)

# COMMAND ----------

assert_widget(run_id, "1. Run ID")

# COMMAND ----------

# MAGIC %md ### Display run details

# COMMAND ----------

from mlflow_tools.display import dump_run

dct = dump_run.dump(
    run_id = run_id, 
    dump_raw = dump_raw,
    artifact_max_level = artifact_max_level, 
    show_tags_as_dict = show_tags_as_dict,
    explode_json_string = explode_json_string,
    format = format
)

# COMMAND ----------

# MAGIC %md ### Write output to file

# COMMAND ----------

write_file(dct, output_file, format)
