"""
Test the MLflow object iterators (Run, Experiment, Registered Model and Model Versions).
"""

from mlflow.entities import ViewType
import mlflow

from mlflow_tools.common.iterators import (
    SearchExperimentsIterator,
    SearchRegisteredModelsIterator,
    #SearchModelVersionsIterator,
    SearchRunsIterator
)
from iterators_test_utils import (
    list_experiments, 
    create_experiment, 
    delete_experiments, 
    delete_models,
    mk_test_object_name_default, 
    TEST_OBJECT_PREFIX
)

client = mlflow.client.MlflowClient()

# ==== Test SearchExperimentsIterator

def _create_experiment(num_runs=5):
    experiment = create_experiment(client)
    for _ in range(0, num_runs):
        with mlflow.start_run():
            mlflow.log_metric("m1", 0.1)
    return experiment

def _create_experiments(num_experiments):
    delete_experiments(client)
    experiments = list_experiments(client)
    assert len(experiments) == 0
    for _ in range(0,num_experiments):
        _create_experiment()

def _run_test_search_experiments(num_experiments, max_results):
    _create_experiments(num_experiments)
    experiments1 = list_experiments(client)
    experiments2 = SearchExperimentsIterator(client, max_results=max_results)
    assert len(experiments1) == len(list(experiments2))


def test_search_experiments_max_results_LT_num_experiments():
    _run_test_search_experiments(10, 5)

def test_search_experiments_max_results_EQ_num_experiments():
    _run_test_search_experiments(10, 10)

def test_search_experiments_max_results_GT_num_experiments():
    _run_test_search_experiments(10, 20)

def test_search_experiments_max_results_custom():
    num_experiments = 101
    max_results = 20
    _create_experiments(num_experiments)
    experiments1 = list_experiments(client)
    assert len(experiments1) == num_experiments
    experiments2 = SearchExperimentsIterator(client, max_results=max_results)
    assert len(experiments1) == len(list(experiments2))

# ==== Test SearchRegisteredModelsIterator

# == test search models 1

def _init_test_search_models():
    delete_experiments(client)
    delete_models(client)

def _create_models(num_models):
    delete_models(client)
    models = client.search_registered_models()
    assert len(models) == 0
    for _ in range(0, num_models):
        model_name = mk_test_object_name_default()
        client.create_registered_model(model_name)


def test_search_models_like():
    _init_test_search_models()
    num_models = 10
    max_results = 5
    _create_models(num_models)
    models = list(SearchRegisteredModelsIterator(client, max_results))
    new_prefix = f"{TEST_OBJECT_PREFIX}_new"
    for j in range(0,4):
        new_name = models[j].name.replace(TEST_OBJECT_PREFIX, new_prefix)
        client.rename_registered_model(models[j].name, new_name)
    filter = f"name like '{new_prefix}%'"
    models2 = SearchRegisteredModelsIterator(client, max_results, filter)
    assert 4 == len(list(models2))

# == test search models 2

def _run_test_search_models(num_models, max_results):
    _create_models(num_models)
    models1 = client.search_registered_models()
    assert len(models1) == num_models
    models2 = SearchRegisteredModelsIterator(client, max_results)
    assert len(models1) == len(list(models2))


def test_search_models_max_results_LT_num_models():
    _run_test_search_models(10, 5)

def test_search_models_max_results_EQ_num_models():
    _run_test_search_models(10, 10)

def test_search_models_max_results_GT_num_models():
    _run_test_search_models(10, 20)

def test_search_models_max_results_custom():
    num_models = 101
    max_results = 20
    _create_models(num_models)
    models1 = client.search_registered_models(max_results=num_models)
    assert len(models1) == num_models
    models2 = SearchRegisteredModelsIterator(client, max_results)
    assert len(models1) == len(list(models2))

def test_search_models_max_results_non_default():
    MAX_RESULTS_DEFAULT = 100
    num_models = 101
    max_results = 20
    _create_models(num_models)
    models1 = client.search_registered_models()
    assert len(models1) == MAX_RESULTS_DEFAULT
    models2 = SearchRegisteredModelsIterator(client, max_results)
    assert len(list(models2)) == num_models

# ==== Test SearchModelVersionsIterator - TODO


# ==== Test SearchRunsIterator

def test_search_runs():
    num_runs = 120
    max_results = 22
    exp = _create_experiment(num_runs)
    runs = client.search_runs(exp.experiment_id)
    assert num_runs == len(runs)
    iterator = SearchRunsIterator(client, exp.experiment_id, max_results)
    runs = list(iterator)
    assert num_runs == len(runs)

def test_runs_search_empty():
    num_runs = 0
    max_results = 22
    exp = _create_experiment(num_runs)
    runs = client.search_runs(exp.experiment_id)
    assert num_runs == len(runs)
    iterator = SearchRunsIterator(client, exp.experiment_id, max_results)
    runs = list(iterator)
    assert num_runs == len(runs)


_num_runs = 5
_num_runs_deleted = 2

def _run_test_deleted_runs():
    exp = _create_experiment(_num_runs)
    runs = list(SearchRunsIterator(client, exp.experiment_id))
    assert _num_runs == len(runs)
    for j in range(0,_num_runs_deleted):
        client.delete_run(runs[j].info.run_id)
    return exp, runs


def test_deleted_runs_default():
    exp, runs = _run_test_deleted_runs()
    runs = list(SearchRunsIterator(client, exp.experiment_id))
    assert _num_runs - _num_runs_deleted == len(runs)

def test_deleted_runs_view_active_only():
    exp, runs = _run_test_deleted_runs()
    runs = list(SearchRunsIterator(client, exp.experiment_id, view_type=ViewType.ACTIVE_ONLY))
    assert _num_runs - _num_runs_deleted == len(runs)

def test_deleted_runs_view_deleted_only():
    exp, runs = _run_test_deleted_runs()
    runs = list(SearchRunsIterator(client, exp.experiment_id, view_type=ViewType.DELETED_ONLY))
    assert _num_runs_deleted == len(runs)

def test_deleted_runs_view_all():
    exp, runs = _run_test_deleted_runs()
    runs = list(SearchRunsIterator(client, exp.experiment_id, view_type=ViewType.ALL))
    assert _num_runs == len(runs)


# Stress test - fails because of connection timeout 
def __test_search_runs_too_many():
    num_runs = 1200
    max_results = 500
    exp = _create_experiment(num_runs)
    runs = client.search_runs(exp.experiment_id)
    assert len(runs) == 1000
    iterator = SearchRunsIterator(client, exp.experiment_id, max_results)
    runs = list(iterator)
    assert num_runs == len(runs)
