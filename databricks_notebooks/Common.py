# Databricks notebook source
#%pip install git+https:///github.com/amesar/mlflow-tools/#egg=mlflow-tools
%pip install /dbfs/home/andre.mesarovic@databricks.com/lib/wheels/mlflow_tools-1.0.0-py3-none-any.whl

# COMMAND ----------

import mlflow
client = mlflow.MlflowClient()

# COMMAND ----------

def _from_dbfs(path):
    return path.replace("dbfs:","/dbfs")

# COMMAND ----------

def write_csv_file(df, path):
    if path != "":
        print("Writing to:",path)
        with open(_from_dbfs(path), "w", encoding="utf-8") as f:
            df.to_csv(f, index=False)

# COMMAND ----------

def write_file(dct, path, format):
    if not path or path == "":
        return
    idx = path.rfind(".")
    if idx > 0:
        _format = path[idx+1:]
        path = path[0:idx]
        if len(_format) > 0: format = _format
    print(f"Writing to: {path}.{format}")
    from mlflow_tools.display import write_dct
    write_dct(dct, _from_dbfs(path), format)

# COMMAND ----------

def assert_widget(value, name):
    if len(value.rstrip())==0:
        raise Exception(f"ERROR: '{name}' widget is required")

# COMMAND ----------

import mlflow, os
print("mlflow version:", mlflow.__version__)
print("DATABRICKS_RUNTIME_VERSION:", os.environ.get("DATABRICKS_RUNTIME_VERSION",None))

# COMMAND ----------

def create_databrick_config_file(secrets_scope, secrets_key, databricks_config_file=None):
    """ Create a .databrickscfg file so you can work in shell mode with Python scripts. """
    context = dbutils.notebook.entry_point.getDbutils().notebook().getContext()
    token = dbutils.secrets.get(scope=secrets_scope, key=secrets_key)
    host_name = context.tags().get("browserHostName").get()
    user = context.tags().get("user").get()

    import os
    if not databricks_config_file:
        databricks_config_file = os.path.join("/tmp", f".databricks.cfg-{user}")
    print(f"DATABRICKS_CONFIG_FILE: {databricks_config_file}")
    os.environ["DATABRICKS_CONFIG_FILE"] = databricks_config_file
    dbutils.fs.put(f"file:///{databricks_config_file}",f"[DEFAULT]\nhost=https://{host_name}\ntoken = "+token,overwrite=True)

# COMMAND ----------

def assert_widget(value, name):
    if len(value.rstrip())==0:
        raise RuntimeError(f"ERROR: '{name}' widget is required")

# COMMAND ----------

def dump_tags(dct):
    if not dct:
        return
    dct = dict(sorted(dct.items()))
    for k,v in dct.items():
        print(f"  {k}: {v}")
