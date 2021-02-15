# mlflow-tools - FailedRunReplayer
  
Save run details for MLflow rate limited exceptions and replay later.

## Overview
* Designed for a rate limited MLflow tracking server that is returning an HTTP 429 (Too Many Requests) code.
  * Designed for recoverable errors where you can safely retry and expect to succeed.
* Best suited for UDFs when you create MLflow runs in the UDF and overwhelm the Databricks MLflow tracking server with concurrent requests.
* Upon a 429, saves run details for failed runs.
  * Saves params, metrics, tags, model, (model name, log_model function), artifacts and run name.
  * Run details are saved in a pickle file.
* Replay the saved run details and create MLflow runs.
* For more usage details see [tests/failed_run_replayer](../../tests/failed_run_replayer).
* For Databricks see [MLflow Rate Limits](https://docs.databricks.com/dev-tools/api/latest/mlflow.html#rate-limits) documentation.

## Example

```
def train(degree, replay_dir):
   ...
   model = svm.SVC(degree=degree, kernel="rbf")
   with open("pickled_prophet.pkl","wb") as f:
       pickle.dump(model,f)
   params = { "degree": str(degree) }
   metrics = { "accuracy": 0.91 }
   # Only put mlflow calls in the try
   try:  
       with mlflow.start_run(experiment_id = mlflow_id) as run:
           mlflow.log_params(params)
           mlflow.log_artifact("myartifact.txt")
   except mlflow.exceptions.MlflowException as ex:
        if "error code 429 != 200" in str(ex):
            # If call fails in mlflow.start_run we won't be inside a run
            run_id = run.info.run_id if "run" in locals() else None
            SaveFailedRunReplayer.save_run(replay_dir, run_id, RunDetails(ex, params=params, metric=metrics, 
                models = [ModelDetails(model, "model", mlflow.sklearn.log_model)]
                artifacts = [ArtifactDetails("myartifact.txt")]))
        else:
            raise(ex)

replayer = CreateFailedRunReplayer("/dbfs/misc/failed_runs")
df = spark.createDataFrame([[j] for j in range(0,10)], ["degree"])
train_udf = F.udf(train)
result = df.withColumn("run_id", train_udf(df["degree"], F.lit(exp.experiment_id), F.lit(replay_dir)
run_ids = replayer.create_runs()
```
