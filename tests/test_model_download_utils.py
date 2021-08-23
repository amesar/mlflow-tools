from mlflow_tools.common.model_download_utils import split_model_uri

def test_split_runs_1():
    _test_split("runs","18f6b9a2f72f44de8bb9591d163c6754", "sklearn-model")

def test_split_runs_2():
    _test_split("runs","18f6b9a2f72f44de8bb9591d163c6754", "models/sklearn-model")

def test_split_models_1():
    _test_split("models","my-model", "1")

def test_split_models_2():
    _test_split("models","my-model", "production")

def test_split_file():
    uri = "/opt/mlflow/mlruns/1/18f6b9a2f72f44de8bb9591d163c6754/artifacts"
    result = split_model_uri(uri)

def _test_split(scheme, p1, p2):
    uri = f"{scheme}:/{p1}/{p2}"
    result = split_model_uri(uri)
    assert result[0] == p1
    assert result[1] == p2

# requires client - TODO
"""
def test_get_run_id_and_relative_path():
    models_uri = "models:/sklearn_wine/production"
    result = get_run_id_and_relative_path(models_uri)
"""
