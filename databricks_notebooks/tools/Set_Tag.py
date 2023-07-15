# Databricks notebook source
# MAGIC %md ## Set Tag of an MLflow object

# COMMAND ----------

# MAGIC %run ../Common

# COMMAND ----------

# MAGIC %md ### Widgets

# COMMAND ----------

dbutils.widgets.dropdown("1. MLflow object", "Registered Model", ["Registered Model", "Model Version", "Experiment", "Run"])
object = dbutils.widgets.get("1. MLflow object")

dbutils.widgets.text("2. Registered Model", "")
model_name = dbutils.widgets.get("2. Registered Model")

dbutils.widgets.text("3. Model Version", "")
model_version = dbutils.widgets.get("3. Model Version")

dbutils.widgets.text("4. Experiment ID or name", "")
experiment_id_or_name = dbutils.widgets.get("4. Experiment ID or name")

dbutils.widgets.text("5. Run ID", "")
run_id = dbutils.widgets.get("5. Run ID")

dbutils.widgets.text("6. Tag key", "")
tag_key = dbutils.widgets.get("6. Tag key")

dbutils.widgets.text("7. Tag value", "")
tag_value = dbutils.widgets.get("7. Tag value")

dbutils.widgets.dropdown("8. Show all tags", "yes", ["yes", "no"])
show_all_tags = dbutils.widgets.get("8. Show all tags") == "yes"

print("object:", object)
print("model_name:", model_name)
print("model_version:", model_version)
print("experiment_id_or_name:", experiment_id_or_name)
print("run_id:", run_id)
print("tag_key:", tag_key)
print("tag_value:", tag_value)
print("show_all_tags:", show_all_tags)

# COMMAND ----------

# MAGIC %md ### Assert widgets

# COMMAND ----------

def assert_widgets():
    if object == "Model":
        assert_widget(model_name, "Missing '2. Model' widget")
    elif object == "Version":
        assert_widget(model_name, "Missing '2. Model' widget")
        assert_widget(model_version, "Missing '3. Version' widget")
    elif object == "Experiment":
        assert_widget(experiment_id_or_name, "Missing '4. Experiment' widget")
    elif object == "Run":
        assert_widget(run_id, "Missing '5. Run ID")
assert_widgets()
assert_widget(tag_key, "Missing '6. Tag key")

# COMMAND ----------

# MAGIC %md ### Define functions

# COMMAND ----------

def show_tags():
    if object == "Registered Model":
        from mlflow_tools.display import dump_registered_model
        dct = dump_registered_model.dump(model_name, silent=True)
        tags = dct.get("tags")
    elif object == "Model Version":
        from mlflow_tools.display import dump_model_version
        dct = dump_model_version.dump(model_name, model_version, silent=True)
        tags = dct["model_version"].get("tags")
    elif object == "Experiment":
        from mlflow_tools.display import dump_experiment
        dct = dump_experiment.dump(experiment_id_or_name, dump_runs=False, silent=True)
        tags = dct["experiment"].get("tags")
    elif object == "Run":
        from mlflow_tools.display import dump_run
        dct = dump_run.dump(run_id, silent=True)
        tags = dct["run"]["data"].get("tags")
    else:
        tags = {}
    if show_all_tags:
        dump_tags(tags)
    else:
        v = tags.get(tag_key)
        print(f"{tag_key}: {v}")

# COMMAND ----------

# MAGIC %md ### Show current tags

# COMMAND ----------

show_tags()

# COMMAND ----------

# MAGIC %md ### Set object tag

# COMMAND ----------

if object == "Registered Model":
    client.set_registered_model_tag(model_name, tag_key, tag_value)
elif object == "Model Version":
    client.set_model_version_tag(model_name, model_version, tag_key, tag_value)
elif object == "Experiment":
    from mlflow_tools.common import mlflow_utils
    exp = mlflow_utils.get_experiment(client, experiment_id_or_name)
    if exp is None:
        raise MlflowToolsException(f"Cannot find experiment '{experiment_id_or_name}'")
    client.set_experiment_tag(exp.experiment_id, tag_key, tag_value)
elif object == "Run":
    client.set_tag(run_id, tag_key, tag_value)

# COMMAND ----------

# MAGIC %md ### Show new tags

# COMMAND ----------

show_tags()
