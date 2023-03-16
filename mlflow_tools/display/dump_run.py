"""
Dump a run in JSON, YAML or text.
"""

import json
import click
from mlflow_tools.client.http_client import MlflowHttpClient
from mlflow_tools.common.timestamp_utils import fmt_ts_millis
from mlflow_tools.common import mlflow_utils
from mlflow_tools.common.click_options import opt_show_tags_as_dict
from . import dump_dct, show_mlflow_info
from . import dump_run_as_text

# Tags to explode from JSON string
explode_tags = [ "mlflow.databricks.cluster.info", "mlflow.databricks.cluster.libraries", "mlflow.log-model.history" ]

http_client = MlflowHttpClient()


def _adjust_time(info, k):
    v = info.get(k,None)
    if v is not None:
        v = fmt_ts_millis(int(v))
    info[f"_{k}"] = v


def adjust_times(info):
    start = info.get("start_time",None)
    end = info.get("end_time",None)
    _adjust_time(info, "start_time")
    _adjust_time(info, "end_time")
    if start is not None and end is not None:
        dur = float(int(end) - int(start))/1000
        info["_duration"] = dur


def _explode_json_string(run):
    for tag in run["data"]["tags"]:
        if tag["key"] in explode_tags:
            tag["value"] = json.loads(tag["value"])


def build_run(
        run, 
        artifact_max_level, 
        explode_json_string,
        show_tags_as_dict = False
    ):
    """
    Returns dict representation of run.
    """
    info = run["info"]
    data = run["data"]
    run_id = info["run_id"]
    adjust_times(info)

    if explode_json_string:
        _explode_json_string(run)

    if show_tags_as_dict:
        run["data"]["tags"] = mlflow_utils.mk_tags_dict(run["data"]["tags"])

    if artifact_max_level == 0:
        num_bytes = -1
        num_artifacts= -1
        summary = { 
            "artifacts": -1, 
            "artifact_bytes": -1,
            "params": _get_size(data.get("params",None)),
            "metrics": _get_size(data.get("metrics",None)),
            "tags": _get_size(data.get("tags",None)),
        }
        dct = { "summary": summary, "run": run }
    else:
        artifacts,num_bytes,num_artifacts = build_artifacts(run_id, "", 0, artifact_max_level)
        summary = { 
            "artifacts": num_artifacts, 
            "artifact_bytes": num_bytes,
            "params": _get_size(data.get("params",None)),
            "metrics": _get_size(data.get("metrics",None)),
            "tags": _get_size(data.get("tags",None)),
        }
        dct = { "summary": summary, "run": run, "artifacts": artifacts }
    return dct


def _get_size(dct):
    return len(dct) if dct else 0


def build_artifacts(run_id, path, level, artifact_max_level):
    artifacts = http_client.get(f"artifacts/list?run_id={run_id}&path={path}")
    if level+1 > artifact_max_level: 
        return artifacts, 0, 0
    num_bytes, num_artifacts = (0,0)
    files = artifacts.get("files",None)
    if files:
        for _,artifact in enumerate(files):
            num_bytes += int(artifact.get("file_size",0)) or 0
            if artifact["is_dir"]:
                arts,b,a = build_artifacts(run_id, artifact["path"], level+1, artifact_max_level)
                num_bytes += b
                num_artifacts += a
                artifact["artifacts"] = arts
            else:
                num_artifacts += 1
    return artifacts, num_bytes, num_artifacts


def dump_run_id(
        run_id, 
        artifact_max_level=1, 
        format="json", 
        explode_json_string = False,
        show_tags_as_dict = False,
    ):
    if (format in ["text","txt"]):
        dump_run_as_text.dump_run_id(run_id, artifact_max_level)
        return ""
    else:
        run = http_client.get(f"runs/get?run_id={run_id}")["run"]
        dct = build_run(run, artifact_max_level, explode_json_string, show_tags_as_dict)
        dump_dct(dct, format)
        return dct


@click.command()
@click.option("--run-id", help="Run ID.", required=True)
@click.option("--artifact-max-level", help="Number of artifact levels to recurse.", default=1, type=int, show_default=True)
@click.option("--format", help="Output Format: json|yaml|txt.", type=str, default="json", show_default=True)
@click.option("--explode-json-string", help="Explode JSON string.", type=bool, default=False, show_default=True)
@click.option("--verbose", help="Verbose.", type=bool, default=False, show_default=False)
@opt_show_tags_as_dict

def main(run_id, artifact_max_level, format, explode_json_string, show_tags_as_dict, verbose):
    if verbose: 
        show_mlflow_info()
        print("Options:")
        for k,v in locals().items(): print(f"  {k}: {v}")
    dump_run_id(run_id, artifact_max_level, format, explode_json_string, show_tags_as_dict)


if __name__ == "__main__":
    main()
