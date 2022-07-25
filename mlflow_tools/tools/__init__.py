import time
import json
import yaml

DT_FORMAT = "%Y-%m-%d %H:%M:%S"

def format_dt(millis):
    return time.strftime(DT_FORMAT,time.gmtime(millis/1000))


def dump_dct(dct, format="json"):
    if format == "yaml":
        print(yaml.safe_dump(dct, sort_keys=False))
    else:
        print(json.dumps(dct,indent=2))


def write_dct(dct, base_path, format="json"):
    path = base_path if base_path.endswith(format) else f"{base_path}.{format}"
    with open(path, "w") as f:
        if format == "yaml":
            yaml.dump(dct, f)
        else:
            f.write(json.dumps(dct, indent=2)+"\n")
    

def show_mlflow_info():
    import mlflow
    print("MLflow Version:", mlflow.version.VERSION)
    print("MLflow Tracking URI:", mlflow.get_tracking_uri())
