# Databricks notebook source
# MAGIC %sh 
# MAGIC pip install git+https:///github.com/amesar/mlflow-tools/#egg=mlflow-tools

# COMMAND ----------

def from_dbfs(path):
    return path.replace("dbfs:","/dbfs")

# COMMAND ----------

def write_csv_file(df, path):
    if path != "":
        print("Writing to:",path)
        with open(from_dbfs(path), "w", encoding="utf-8") as f:
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
    from mlflow_tools.tools import write_dct
    write_dct(dct, from_dbfs(path), format)