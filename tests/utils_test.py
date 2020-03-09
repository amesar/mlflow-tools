
import mlflow
print("Mlflow path:", mlflow.__file__)
print("MLflow version:", mlflow.__version__)

client = mlflow.tracking.MlflowClient()
count = 0

def create_experiment():
    global count
    exp_name = f"test_exp_{count}"
    count += 1
    mlflow.set_experiment(exp_name)
    exp = client.get_experiment_by_name(exp_name)
    for info in client.list_run_infos(exp.experiment_id):
        client.delete_run(info.run_id)
    return exp

def create_runs():
    create_experiment()
    with mlflow.start_run() as run:
        mlflow.log_param("p1", "hi")
        mlflow.log_metric("m1", 0.786)
        mlflow.set_tag("t1", "hi")
    return client.search_runs(run.info.experiment_id, "")

def delete_experiment(exp):
    client.delete_experiment(exp.experiment_id)
