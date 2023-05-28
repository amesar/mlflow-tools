import os
from tempfile import NamedTemporaryFile
import mlflow
from mlflow_tools.display.display_utils import build_artifacts
from . utils_test import create_experiment

content = "the 14 eight-thousanders"
content_size = len(content)

# == Test no levels

def test_no_artifacts():
    create_experiment()
    with mlflow.start_run() as run:
        mlflow.log_metric("m1", 0.1)
    res = build_artifacts(run.info.run_id, "", 0)
    _assert_result(res, 0, 0, 0, 0)


# == Test one level

def _create_level_1():
    create_experiment()
    with NamedTemporaryFile(prefix="file_", suffix=".txt", mode="w") as f:
        with mlflow.start_run() as run:
            _log_artifact(f, "")
    return run, f.name

def test_level_1_one_file():
    run, _ = _create_level_1()
    res = build_artifacts(run.info.run_id, "", 0)
    _assert_result(res, 0, 0, 0, 0)

def test_level_1_two_files():
    run, file_name = _create_level_1()
    res = build_artifacts(run.info.run_id, "", 1)
    _assert_result(res, content_size, 1, 1, 1)
    artifact = _find_file(res)
    assert artifact["file_size"] == content_size
    assert artifact["path"] == os.path.basename(file_name)


# == Test two levels

def _create_level_2():
    create_experiment()
    with NamedTemporaryFile(prefix="file_1_", suffix=".txt", mode="w") as f:
        with mlflow.start_run() as run:
            _log_artifact(f, "")
            with NamedTemporaryFile(prefix="file_2_", suffix=".txt", mode="w") as f2:
                _log_artifact(f2, "model")
    return run

def test_level_2_one_file():
    run = _create_level_2()
    res = build_artifacts(run.info.run_id, "", 1)
    _assert_result(res, content_size, 1, 1, 1)
    assert len(res["files"]) == 2

    artifact = _find_dir(res)
    assert artifact["path"] == "model"
    artifact = _find_file(res)
    assert artifact["file_size"] == content_size

def test_level_2_two_files():
    run = _create_level_2()
    res = build_artifacts(run.info.run_id, "", 2)
    _assert_result(res, content_size * 2, 2, 2, 2)
    assert len(res["files"]) == 2

    artifact = _find_dir(res)
    assert artifact["path"] == "model"
    artifact = _find_file(res)
    assert artifact["file_size"] == content_size

# == Test three levels

def _create_level_3():
    create_experiment()
    with NamedTemporaryFile(prefix="file_1_",suffix=".txt", mode="w") as f:
        with mlflow.start_run() as run:
            _log_artifact(f, "")
            with NamedTemporaryFile(prefix="file_2a_",suffix=".txt", mode="w") as f2:
                _log_artifact(f2, "model")
            with NamedTemporaryFile(prefix="file_2b_",suffix=".txt", mode="w") as f2:
                _log_artifact(f2, "model")
            with NamedTemporaryFile(prefix="file_3_",suffix=".txt", mode="w") as f2:
                _log_artifact(f2, "model/sklearn")
    return run

def test_level_3_three_files():
    run = _create_level_3()
    res = build_artifacts(run.info.run_id, "", 3)
    _assert_result(res, content_size * 4, 4, 3, 3)
    assert len(res["files"]) == 2
    artifact = _find_dir(res)
    assert artifact["path"] == "model"


# == Helper functions

def _find_file(res):
    matches = [x for x in res["files"] if not x["is_dir"] ]
    return matches[0]

def _find_dir(res):
    matches = [x for x in res["files"] if x["is_dir"] ]
    return matches[0]

def _log_artifact(f, artifact_path):
    f.file.write(content)
    f.file.close()
    mlflow.log_artifact(f.name, artifact_path)

def _assert_result(res, num_bytes, num_artifacts, num_levels, artifact_max_level):
    res = res["summary"]
    assert res["artifact_max_level"] == artifact_max_level
    assert res["num_bytes"] == num_bytes
    assert res["num_artifacts"] == num_artifacts
    assert res["num_levels"] == num_levels
