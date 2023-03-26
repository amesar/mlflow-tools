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
# MAGIC * `Artifact max level` - number of artifact levels to show
# MAGIC * `Format` - JSON or YAML
# MAGIC * `Output file` - if set, write output to file

# COMMAND ----------

# MAGIC %run ../Common

# COMMAND ----------

# MAGIC %md ### Widgets

# COMMAND ----------

#dbutils.widgets.removeAll()


# COMMAND ----------

dbutils.widgets.text("1. Run ID", "")
dbutils.widgets.dropdown("2. Show tags as dictionary","no",["yes","no"])
dbutils.widgets.text("3. Artifact max level", "1")
dbutils.widgets.dropdown("4. Format","json",["json","yaml"])
dbutils.widgets.text("5. Output file", "")

run_id = dbutils.widgets.get("1. Run ID")
show_tags_as_dict = dbutils.widgets.get("2. Show tags as dictionary") == "yes"
artifact_max_level = int(dbutils.widgets.get("3. Artifact max level"))
format = dbutils.widgets.get("4. Format")
output_file = dbutils.widgets.get("5. Output file")

print("run_id:", run_id)
print("show_tags_as_dict:", show_tags_as_dict)
print("artifact_max_level:", artifact_max_level)
print("format:", format)
print("output_file:", output_file)

# COMMAND ----------

assert_widget(run_id, "1. Run ID")

# COMMAND ----------

# MAGIC %md ### Display run details

# COMMAND ----------

from mlflow_tools.display import dump_run

dct = dump_run.dump_run_id(
    run_id = run_id, 
    show_tags_as_dict = show_tags_as_dict,
    artifact_max_level = artifact_max_level, 
    format = format,
    explode_json_string = False
)

# COMMAND ----------

# MAGIC %md ### Write output to file

# COMMAND ----------

write_file(dct, output_file, format)
