import pickle
import random
from sklearn import svm, datasets
import mlflow
from mlflow.exceptions import MlflowException
from mlflow_tools.failed_run_replayer import SaveFailedRunReplayer
from mlflow_tools.failed_run_replayer import RunDetails, ModelDetails, ArtifactDetails

print("MLflow Tracking URI:", mlflow.get_tracking_uri())
client = mlflow.tracking.MlflowClient()

error_msg = "failed with error code 429 != 200"
replay_dir = "out"
num_records = 10
data = [[j] for j in range(0,num_records)]

def raise_exceptions_udf(idx, raise_mlflow_429_ex, raise_mlflow_non_429_ex, raise_non_mlflow_ex):
    """Test throwing different exceptions"""
    if raise_mlflow_429_ex and idx % 4 == 0: raise MlflowException(f"{error_msg} {idx}")
    if raise_mlflow_non_429_ex and idx == 4: raise MlflowException(f"Ouch - mlflow_non_429: {idx}")
    if raise_non_mlflow_ex and idx == 5: raise NotImplementedError(f"Ouch - non_mlflow: {idx}")

def raise_exceptions_non_udf(idx, raise_mlflow_429_ex, raise_mlflow_non_429_ex, raise_non_mlflow_ex):
    """Test throwing different exceptions"""
    if raise_mlflow_429_ex and idx % 4 == 0: raise MlflowException(f"{error_msg} {idx}")
    if raise_mlflow_non_429_ex and idx == 4: raise MlflowException(f"Ouch - mlflow_non_429: {idx}")
    if raise_non_mlflow_ex and idx == 5: raise NotImplementedError(f"Ouch - non_mlflow: {idx}")

def train(idx, experiment_id, replay_dir, is_udf, raise_mlflow_429_ex, raise_mlflow_non_429_ex, raise_non_mlflow_ex):
    iris = datasets.load_iris()
    C = round(random.uniform(1,4),3)
    model = svm.SVC(C=C, degree=5, kernel="rbf")
    model.fit(iris.data, iris.target)
    params = { "C": f"v{C}" }
    metrics = { "accuracy": .789 }
    tags = { "index": str(idx) }
    with open("mymodel.pkl","wb") as f:
        pickle.dump(model, f)
    run_name = f"my_run_{idx}"
    try:
        with mlflow.start_run(experiment_id=experiment_id, run_name=run_name) as run:
            mlflow.log_params(params)
            mlflow.log_metrics(metrics)
            if is_udf:
                raise_exceptions_udf(idx, raise_mlflow_429_ex, raise_mlflow_non_429_ex, raise_non_mlflow_ex)
            else:
                raise_exceptions_non_udf(idx, raise_mlflow_429_ex, raise_mlflow_non_429_ex, raise_non_mlflow_ex)
            mlflow.set_tags(tags)
            mlflow.sklearn.log_model(model, "model")
            mlflow.log_artifact("mymodel.pkl")
            return run.info.run_id
    except mlflow.exceptions.MlflowException as ex:
        if error_msg in str(ex):
            # If call fails in mlflow.start_run we won't be inside a run
            run_id = run.info.run_id if "run" in locals() else None
            SaveFailedRunReplayer.save_run(replay_dir, run_id,
                RunDetails(
                    ex,
                    run_name = run_name,
                    params = params,
                    metrics = metrics,
                    tags = tags,
                    models = [ModelDetails(model, "model", mlflow.sklearn.log_model)],
                    artifacts = [ArtifactDetails("mymodel.pkl")]))
            return None
        else:
            raise(ex)

def run_test_no_exception(process):
    replayer,_,runs,ex = process(False, False, False)
    assert not ex
    assert 10 == len(runs)
    failed_runs = replayer.list_run_details()
    assert len(failed_runs) == 0

def run_test_raise_mlflow_429_ex_exception(process):
    replayer,exp,runs,ex = process(True, False, False)
    assert not ex
    assert 7 == len(runs)
    failed_runs = replayer.list_run_details()
    assert len(failed_runs) == 3
    replayed_runs = replayer.create_runs()
    assert len(replayed_runs) == 3
    runs = client.search_runs(exp.experiment_id)
    assert 10 == len(runs)

def dump(replayer):
    import pandas as pd
    failed_runs = replayer.list_run_details()
    pdf = pd.DataFrame.from_dict([run.__dict__ for run in failed_runs])
    print("Replayer Dump")
    print(pdf)
