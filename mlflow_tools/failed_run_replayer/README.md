# mlflow-tools - FailedRunReplayer
  
Save run details for MLflow rate limited exceptions and replay later.

## Overview
* Designed for recoverable errors such HTTP 429 (Too Many Requests).
* When you create MLflow runs in a UDF and overwhelm the Databricks MLflow tracking server with concurrently requests.
* Saves run details for failed runs 
  * Saves params, metrics, tags, model, model name, artifacts and run name.
  * Run details are saved in a pickle file.
* Replay the saved run details and create MLflow runs.
* For more usage details see [tests/failed_run_replayer](../../tests/failed_run_replayer).

## Example

```
replay_dir = "/dbfs/misc/failed_runs"

def train(C, replay_dir):
   ...
   model = svm.SVC(C=C, degree=5, kernel="rbf")
   with open("pickled_prophet.pkl","wb") as f:
       pickle.dump(m,f,protocol=pickle.HIGHEST_PROTOCOL)
   params = { "C": str(C) }
   metrics = { "accuracy": "" }
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

train_udf = F.udf(train)
replayer = CreateFailedRunReplayer(log_dir)
result = df_data.withColumn("run_id", train_udf(df_data["idx"], F.lit(exp.experiment_id), F.lit(replay_dir)
failed_runs = replayer.list_run_details()
```
