"""
Dump a run in JSON or YAML.
"""

import json
import click

from mlflow_tools.client.http_client import MlflowHttpClient
from mlflow_tools.common.timestamp_utils import fmt_ts_millis
from mlflow_tools.common import mlflow_utils
from mlflow_tools.common.mlflow_utils import parse_sparkDatasourceInfo_tag
from mlflow_tools.common.click_options import (
    opt_artifact_max_level,
    opt_show_tags_as_dict,
    opt_explode_json_string,
    opt_format,
    opt_output_file,
    opt_show_system_info
)
from mlflow_tools.display.display_utils import build_artifacts
from mlflow_tools.display.display_utils import dump_finish


# Tags to explode from JSON string
explode_tags = [ 
    "mlflow.databricks.cluster.info", 
    "mlflow.databricks.cluster.libraries", 
    "mlflow.log-model.history",
    "mlflow.datasets"
]

http_client = MlflowHttpClient()


def _adjust_time(info, k):
    v = info.get(k)
    if v is not None:
        v = fmt_ts_millis(int(v))
    info[f"_{k}"] = v


def adjust_times(info):
    start = info.get("start_time")
    end = info.get("end_time")
    _adjust_time(info, "start_time")
    _adjust_time(info, "end_time")
    if start is not None and end is not None:
        dur = float(int(end) - int(start))/1000
        info["_duration"] = dur


def _explode_json_string_tags(run):
    for tag in run["data"]["tags"]:
        if tag["key"] in explode_tags:
            tag["value"] = json.loads(tag["value"])
            if tag["key"] == "mlflow.log-model.history":
                _explode_history(tag)
        elif tag["key"] == "sparkDatasourceInfo":
            tag["value"] = parse_sparkDatasourceInfo_tag(tag["value"])

def _explode_string_tag(dct, key):
    v = dct.get(key)
    if v:
        dct[key] = json.loads(v)

def _explode_history(tag):
    for tv in tag["value"]:
        v = tv.get("signature")
        if v:
            _explode_string_tag(v, "inputs")
            _explode_string_tag(v, "outputs")

def _adjust_inputs(run, explode_json_string, show_tags_as_dict):
    """ Adjust new MLflow 2.4.0 run attribute 'inputs' """
    if not explode_json_string and not show_tags_as_dict:
        return
    inputs = run.get("inputs")
    if inputs is None:
        return
    dataset_inputs = inputs.get("dataset_inputs")
    if dataset_inputs is None:
        return
    for di in dataset_inputs:
        if explode_json_string:
            ds = di.get("dataset")
            if ds:
                _explode_string_tag(ds, "source")
                _explode_string_tag(ds, "schema")
                _explode_string_tag(ds, "profile")
        if show_tags_as_dict:
            tags = di.get("tags")
            if tags:
                di["tags"] = mlflow_utils.mk_tags_dict(tags)


def build_run(run, explode_json_string=True, show_tags_as_dict=True):
    """
    Returns adjusted dict representation of run.
    """
    info = run["info"]
    adjust_times(info)

    exp = http_client.get("experiments/get", {"experiment_id": info["experiment_id"]}) ["experiment"]
    run["info"]["_experiment_name"] = exp["name"]

    if explode_json_string:
        _explode_json_string_tags(run)
    if show_tags_as_dict:
        run["data"]["tags"] = mlflow_utils.mk_tags_dict(run["data"]["tags"])
    _adjust_inputs(run, explode_json_string, show_tags_as_dict)
    return run


def build_run_extended(
        run,
        artifact_max_level = 1,
        explode_json_string = True,
        show_tags_as_dict = True
    ):
    def _get_size(dct):
        return len(dct) if dct else 0

    run  = build_run(run, explode_json_string, show_tags_as_dict)
    data = run["data"]
    run_id = run["info"]["run_id"]

    artifacts = build_artifacts(run_id, "", artifact_max_level)
    summary = {
        "params": _get_size(data.get("params")),
        "metrics": _get_size(data.get("metrics")),
        "tags": _get_size(data.get("tags")),
        "artifacts": artifacts["summary"]
    }
    return { 
        "summary": summary, 
        "run": run, 
        "artifacts": artifacts
    }


def dump(
        run_id,
        artifact_max_level = 1,
        explode_json_string = False,
        show_tags_as_dict = False,
        show_system_info = False,
        format = "json",
        output_file = None
    ):
    """
    :param run_id: Run ID.
    :return: Dictionary of run details 
    """
    run = http_client.get(f"runs/get", { "run_id": run_id })
    dct = build_run_extended(run["run"], artifact_max_level, explode_json_string, show_tags_as_dict)

    dct = dump_finish(dct, output_file, format, show_system_info, __file__)
    return dct


@click.command()
@click.option("--run-id",
    help="Run ID.",
    type=str,
    required=True
)
@opt_artifact_max_level
@opt_explode_json_string
@opt_show_tags_as_dict
@opt_show_system_info
@opt_format
@opt_output_file

def main(run_id, artifact_max_level, explode_json_string, show_tags_as_dict, show_system_info, format, output_file):
    print("Options:")
    for k,v in locals().items():
        print(f"  {k}: {v}")
    dump(run_id, artifact_max_level, explode_json_string, show_tags_as_dict, show_system_info, format, output_file)


if __name__ == "__main__":
    main()
