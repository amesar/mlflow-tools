import mlflow
from mlflow.exceptions import MlflowException
from mlflow_tools.failed_run_replayer import CreateFailedRunReplayer
from tests.utils_test import create_experiment
from . common import train, run_test_no_exception, run_test_raise_mlflow_429_ex_exception, dump
from . common import client, error_msg, replay_dir, data

def process(raise_mlflow_429_ex, raise_mlflow_non_429_ex, raise_non_mlflow_ex):
    exp = create_experiment()
    replayer = CreateFailedRunReplayer(replay_dir)
    replayer.remove_files()
    mlflow.set_experiment(exp.name)
    exp = client.get_experiment_by_name(exp.name)
    try:
        for idx in data:
            train(idx[0], exp.experiment_id, replay_dir, False, raise_mlflow_429_ex, raise_mlflow_non_429_ex, raise_non_mlflow_ex)
        ex = None
    except Exception as e:
        ex = e
    runs = client.list_run_infos(exp.experiment_id)
    return replayer,exp,runs,ex

def test_no_exception():
    run_test_no_exception(process)

def test_raise_mlflow_429_ex_exception():
    run_test_raise_mlflow_429_ex_exception(process)

def test_raise_mlflow_non_429_ex_exception():
    replayer,_,runs,ex = process(False, True, False)
    #dump(replayer)
    assert ex and isinstance(ex,MlflowException) and not error_msg in str(ex)
    assert 5 == len(runs)
    failed_runs = replayer.list_run_details()
    assert len(failed_runs) == 0

def test_raise_non_mlflow_ex_exception():
    replayer,_,runs,ex = process(False, False, True)
    assert ex and isinstance(ex,NotImplementedError)
    assert 6 == len(runs)
    failed_runs = replayer.list_run_details()
    assert len(failed_runs) == 0
