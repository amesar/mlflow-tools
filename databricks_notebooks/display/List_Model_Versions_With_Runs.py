# Databricks notebook source
# MAGIC %md ## List Model Versions with Runs
# MAGIC 
# MAGIC Analytics about model versions and their runs - have the runs been soft or hard deleted?
# MAGIC 
# MAGIC Widget values:
# MAGIC * `1a. Model (or Filter)` - Model name or "*" for all. Mututally exclusive with `Filter`. Example: `andre_02a_Sklearn_Train_Predict`.
# MAGIC * `1b. Filter (or Model)` - Search filter. Mututally exclusive with `Model`. Example: `name like 'andre%'`
# MAGIC * `2. Get versions` - Retrieve "all" or just the "latest" versions.
# MAGIC 
# MAGIC For more details: [github.com/amesar/mlflow-tools/display/README#List-model-versions-with-runs](https://github.com/amesar/mlflow-tools/blob/master/mlflow_tools/display/README.md#List-model-versions-with-runs)

# COMMAND ----------

# MAGIC %md ### Setup

# COMMAND ----------

# MAGIC %run ./Common

# COMMAND ----------

# MAGIC %md ### Widgets

# COMMAND ----------

dbutils.widgets.text("1a. Model (or Filter)", "")
model = dbutils.widgets.get("1a. Model (or Filter)")

dbutils.widgets.text("1b. Filter (or Model)", "")
filter = dbutils.widgets.get("1b. Filter (or Model)") 

dbutils.widgets.dropdown("2. Get versions", "All versions", ["All versions","Latest versions"])
get_latest_versions = dbutils.widgets.get("2. Get versions") == "Latest versions"

dbutils.widgets.dropdown("2. Get versions", "All versions", ["All versions","Latest versions"])
get_latest_versions = dbutils.widgets.get("2. Get versions") == "Latest versions"

if model == "": model = None
if filter == "": filter = None
print("model:", model)
print("filter:", filter)
print("get_latest_versions:", get_latest_versions)

# COMMAND ----------

# MAGIC %md ### Fetch data

# COMMAND ----------

from mlflow_tools.display.list_model_versions_with_runs import to_pandas_dataframe
pdf = to_pandas_dataframe(
    model_names = model, 
    filter = filter, 
    get_latest_versions = get_latest_versions
)
df = spark.createDataFrame(pdf)
display(df)

# COMMAND ----------

# MAGIC %md ### Queries

# COMMAND ----------

df.createOrReplaceTempView("versions") 

# COMMAND ----------

# MAGIC %md #### Show number of versions whose runs don't exist (hard delete)

# COMMAND ----------

# MAGIC %sql select count(*) as run_doesnt_exist from versions where run_exists = 'false' ;

# COMMAND ----------

# MAGIC %md #### Show total summary of versions and runs

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT count(*) total,
# MAGIC   (select count(*) from versions where run_exists = 'false' )  as runs_dont_exist,
# MAGIC   (select count(*) from versions where run_exists = 'true' )  as runs_exist,
# MAGIC   (select count(*) from versions where run_stage = 'deleted' )  as runs_deleted,
# MAGIC   (select count(*) from versions where run_stage = 'active' )  as runs_active
# MAGIC from (SELECT * FROM versions) x

# COMMAND ----------

# MAGIC %md #### Show per model summary of versions and runs

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT model,
# MAGIC   (select count(*) from versions where run_exists = 'false' and model=x.model )  as runs_dont_exist,
# MAGIC   (select count(*) from versions where run_exists = 'true' and model=x.model)  as runs_exist,
# MAGIC   (select count(*) from versions where run_stage = 'deleted' and model=x.model)  as runs_deleted,
# MAGIC   (select count(*) from versions where run_stage = 'active' and model=x.model)  as runs_active
# MAGIC from (SELECT DISTINCT model FROM versions) x
# MAGIC order by runs_dont_exist desc
