import mlflow
import os, shutil
from utils_test import create_experiment
from mlflow_tools.tools.dump_run import dump_run
from mlflow_tools.export_import.export_run import RunExporter
from mlflow_tools.export_import.import_run import RunImporter

client = mlflow.tracking.MlflowClient()
output = "out"

def create_simple_run():
    exp = create_experiment()
    with mlflow.start_run(run_name="my_run") as run:
        mlflow.log_param("p1","0.1")
        mlflow.log_metric("m1", 0.1)
        mlflow.set_tag("my_tag","my_val")
    return exp,run

def init_output_dir():
    if os.path.exists(output):
        shutil.rmtree(output)
    os.makedirs(output)

def init_test(exporter, importer, verbose=False):
    init_output_dir()
    exp, run = create_simple_run()
    exporter.export_run(run.info.run_id, output)

    experiment_name = f"{exp.name}_import" 
    res = importer.import_run(experiment_name, output)
    if verbose: print("res:",res)

    run1 = client.get_run(run.info.run_id)
    run2 = client.get_run(res[0])
    if verbose:
        print("run1:",run1)
        print("run2:",run2)
        print("======= Run1")
        dump_run(run1)
        print("======= Run2")
        dump_run(run2)
    return run1, run2

def test_basic():
    run1, run2 = init_test(RunExporter(), RunImporter())
    compare_runs(run1, run2)

def test_no_import_mlflow_tags():
    run1, run2 = init_test(RunExporter(), RunImporter(import_mlflow_tags=False))
    compare_runs_no_tags(run1, run2)
    assert "mlflow.runName" in run1.data.tags
    assert not "mlflow.runName" in run2.data.tags
    run1.data.tags.pop("mlflow.runName")
    assert run1.data.tags == run2.data.tags

def test_import_metadata_tags():
    run1, run2 = init_test(RunExporter(export_metadata_tags=True), RunImporter(import_metadata_tags=True), verbose=True)
    compare_runs_no_tags(run1, run2)
    metadata_tags = { k:v for k,v in run2.data.tags.items() if k.startswith("mlflow_tools.metadata") }
    assert len(metadata_tags) > 0
    #metadata_tags = { k.replace("mlflow_tools.metadata.",""):v for k,v in run2.data.tags.items() if k.startswith("mlflow_tools.metadata") }
    #assert run1.data.tags == metadata_tags

def compare_runs_no_tags(run1, run2):
    assert run1.info.lifecycle_stage == run2.info.lifecycle_stage
    assert run1.info.status == run2.info.status
    assert run1.data.params == run2.data.params
    assert run1.data.metrics == run2.data.metrics

def compare_runs(run1, run2):
    compare_runs_no_tags(run1, run2)
    assert run1.data.tags == run2.data.tags
