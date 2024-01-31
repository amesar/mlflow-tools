# Databricks notebook source
# MAGIC %md ## Benchmark Model Serving Endpoint - Multitheaded
# MAGIC
# MAGIC * https://e2-demo-west.cloud.databricks.com/ml/endpoints/sklearn_wine_best?o=2556758628403379

# COMMAND ----------

# MAGIC %run ../Common

# COMMAND ----------

import mlflow_tools 
import mlflow_tools.tools
import mlflow_tools.model_serving_benchmarks 

# COMMAND ----------

#dbutils.widgets.removeAll()

dbutils.widgets.text("1. Model Serving Endpoint", "sklearn_wine_best")
endpoint_name = dbutils.widgets.get("1. Model Serving Endpoint")

dbutils.widgets.text("2. Requests", "5")
num_requests = int(dbutils.widgets.get("2. Requests"))

dbutils.widgets.text("3. Threads", "1")
num_threads = int(dbutils.widgets.get("3. Threads"))
 
dbutils.widgets.text("4. Output file base", "out")
output_file_base = dbutils.widgets.get("4. Output file base")

dbutils.widgets.text("5. Log modulo", "20")
log_mod = int(dbutils.widgets.get("5. Log modulo"))
                                       
dbutils.widgets.text("6. Client Request ID", "")
client_request_id = dbutils.widgets.get("6. Client Request ID")  

dbutils.widgets.text("7. Token", "")
token = dbutils.widgets.get("7. Token")

data_path = "sample_data.csv"

print("endpoint_name:", endpoint_name)
print("num_requests:", num_requests)
print("num_threads:", num_threads)
print("data_path:", data_path)
print("output_file_base:", output_file_base)
print("log_mod:", log_mod)
print("client_request_id:", client_request_id)
print("token:", token)

# COMMAND ----------

assert_widget(endpoint_name, "1. Model Serving Endpoint")

# COMMAND ----------

from mlflow.utils import databricks_utils

token = token or dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().get()

workspace_url = databricks_utils.get_workspace_url()
endpoint_uri = f"https://{workspace_url}/serving-endpoints/{endpoint_name}/invocations"
endpoint_uri

# COMMAND ----------

from mlflow_tools.model_serving_benchmarks import benchmark, threaded_benchmark

threaded_benchmark.run(endpoint_uri, 
    token = token,
    data_path = data_path,
    output_file_base = output_file_base, 
    log_mod = log_mod, 
    num_requests = num_requests,
    num_threads = num_threads,
    add_timestamp_to_output_file = False,
    client_request_id = client_request_id
)
