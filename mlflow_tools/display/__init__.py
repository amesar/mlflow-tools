import json
import yaml
import mlflow
from mlflow_tools.common import io_utils


def from_dbfs(path):
    return path.replace("dbfs:","/dbfs")


def write_dct(dct, base_path, format="json"):
    path = base_path if base_path.endswith(format) else f"{base_path}.{format}"
    path = from_dbfs(path)
    io_utils.write_file(path, dct, format)


def dump_dct(dct, format="json"):
    if format == "yaml":
        print(yaml.safe_dump(dct, sort_keys=False))
    else:
        print(json.dumps(dct,indent=2))


def show_mlflow_info():
    print("MLflow Version:", mlflow.version.VERSION)
    print("MLflow Tracking URI:", mlflow.get_tracking_uri())
