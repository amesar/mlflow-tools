import time
import json
import yaml

DT_FORMAT = "%Y-%m-%d %H:%M:%S"

def format_dt(millis):
    return time.strftime(DT_FORMAT,time.gmtime(millis/1000))

def dump_dct(dct, format="json"):
    if format == "yaml":
        print(yaml.safe_dump(dct,sort_keys=False))
    else:
        print(json.dumps(dct,indent=2))

def show_mlflow_info():
    import mlflow
    print("MLflow Version:", mlflow.version.VERSION)
    print("MLflow Tracking URI:", mlflow.get_tracking_uri())
