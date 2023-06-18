import os
from dataclasses import dataclass
from mlflow_tools.client.http_client import MlflowHttpClient
from mlflow_tools.common.timestamp_utils import ts_now_fmt_utc

http_client = MlflowHttpClient()


def build_artifacts(run_id, path, artifact_max_level=10000, level=0):
    """
    Build recursive tree of calls to 'artifacts/list' API endpoint.
    :param run_id: Run ID.
    :param path: Relative artifact path.
    :param artifact_max_level: Levels to recurse.
    :return: Nested dict with list of artifacts representing tree node info.
    """
    res = _build_artifacts(run_id, path, artifact_max_level, level)
    summary = {
        "relative_artifact_path": path,
        "size": res.num_bytes,
        "num_artifacts": res.num_artifacts
    } 
    return { **{ "summary": summary }, **res.artifacts }

def _build_artifacts(run_id, path, artifact_max_level=10000, level=0):
    @dataclass()
    class Result:
        artifacts: dict = None
        num_bytes: int = 0
        num_artifacts: int = 0
        num_levels: int = 0
        def __repr__(self):
            return f"{self.num_bytes} {self.num_artifacts} {self.num_levels}"

    if level == artifact_max_level:
        return Result({}, 0, 0, level)

    artifacts = http_client.get(f"artifacts/list", { "run_id": run_id, "path": path })
    artifacts.pop("root_uri", None)
    if level > artifact_max_level:
        return Result(artifacts, 0, 0, level)

    files = artifacts.get("files", None)
    level += 1
    new_level = level
    num_bytes, num_artifacts = (0,0)

    if files:
        new_files = []
        for _,artifact in enumerate(files):
            num_bytes += int(artifact.get("file_size",0)) or 0
            if artifact["is_dir"]:
                res = _build_artifacts(run_id, artifact["path"], artifact_max_level, level)
                new_level = max(new_level, res.num_levels)
                num_bytes += res.num_bytes
                num_artifacts += res.num_artifacts
                artifact["artifacts"] = res.artifacts
            else:
                num_artifacts += 1
            artifact.pop("is_dir", None)
            artifact.pop("root_uri", None)
            artifact["path"] = artifact["path"].replace(f"{path}/","")
            new_files.append(artifact)
        artifacts["files"] = new_files

    return Result(artifacts, num_bytes, num_artifacts, new_level)


def build_system_info(script):
    import mlflow
    import getpass
    return {
        "script": os.path.basename(script),
        "timestamp": ts_now_fmt_utc,
        "user": getpass.getuser(),
        "mlflow_version": mlflow.__version__
    } 

# https://mlflow.org/docs/latest/rest-api.html#mlflowruninfo
# User who initiated the run. This field is deprecated as of MLflow 1.0, and will be removed in a future MLflow release. Use ‘mlflow.user’ tag instead.

# https://docs.databricks.com/api-explorer/workspace/experiments/getrun
# User who initiated the run. This field is deprecated as of MLflow 1.0, and will be removed in a future MLflow release. Use 'mlflow.user' tag instead.

def get_user(run):
    return run["data"]["tags"].get("mlflow.user")
    #return run["info"].get("user_id")
