"""
Dump a run in JSON or YAML.
"""

import click

from mlflow_tools.client.http_client import MlflowHttpClient
from mlflow_tools.common.timestamp_utils import fmt_ts_millis
from mlflow_tools.common import mlflow_utils, io_utils, object_utils
from mlflow_tools.common.explode_utils import explode_json
from mlflow_tools.common.click_options import (
    opt_dump_raw,
    opt_artifact_max_level,
    opt_show_tags_as_dict,
    opt_explode_json_string,
    opt_format,
    opt_output_file,
    opt_show_system_info
)
from mlflow_tools.display.display_utils import build_artifacts
from mlflow_tools.display.display_utils import dump_finish

http_client = MlflowHttpClient()


def dump(
        run_id,
        dump_raw = False,
        artifact_max_level = 1,
        explode_json_string = True,
        show_tags_as_dict = True,
        show_system_info = False,
        format = "json",
        output_file = None,
        silent = False
    ):
    """
    :param run_id: Run ID.
    :return: Dictionary of run details 
    """
    run = http_client.get(f"runs/get", { "run_id": run_id })
    if dump_raw:
        if output_file:
            io_utils.write_file(output_file, run)
        object_utils.dump_dict_as_json(run)
        return run
    else:
        dct = build_run_extended(run["run"], artifact_max_level, explode_json_string, show_tags_as_dict)
        dct = dump_finish(dct, output_file, format, show_system_info, __file__, silent=silent)
        return dct



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


def build_run(run, explode_json_string=True, show_tags_as_dict=True):
    """
    Returns adjusted dict representation of run.
    """
    if explode_json_string:
        explode_json(run)

    info = run["info"]
    adjust_times(info)

    exp = http_client.get("experiments/get", {"experiment_id": info["experiment_id"]}) ["experiment"]
    run["info"]["_experiment_name"] = exp["name"]

    if show_tags_as_dict:
        run["data"]["tags"] = mlflow_utils.mk_tags_dict(run["data"]["tags"])
    
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


@click.command()
@click.option("--run-id",
    help="Run ID.",
    type=str,
    required=True
)
@opt_dump_raw
@opt_artifact_max_level
@opt_explode_json_string
@opt_show_tags_as_dict
@opt_show_system_info
@opt_format
@opt_output_file

def main(run_id, dump_raw, artifact_max_level, explode_json_string, show_tags_as_dict, show_system_info, format, output_file):
    print("Options:")
    for k,v in locals().items():
        print(f"  {k}: {v}")
    dump(run_id, dump_raw, artifact_max_level, explode_json_string, show_tags_as_dict, show_system_info, format, output_file)


if __name__ == "__main__":
    main()
