import click

from mlflow_tools.client.http_client import MlflowHttpClient
from mlflow_tools.common import mlflow_utils, model_download_utils
from mlflow_tools.common.timestamp_utils import fmt_ts_millis, ts_now_fmt_utc
from mlflow_tools.common.click_options import (
    opt_show_system_info,
    opt_format,
    opt_output_file
)        
from mlflow_tools.display import dump_run
from mlflow_tools.display import dump_registered_model as _dump_registered_model
from mlflow_tools.display import dump_mlflow_model as _dump_mlflow_model
from mlflow_tools.display.display_utils import dump_finish
from mlflow_tools.reports import report_utils

http_client = MlflowHttpClient()


def build_report(model_name, version):
    """
    Build the model version report
    :return: Dictionary of version report 
    """
    rsp = http_client.get("model-versions/get", { "name": model_name, "version": version })
    vr = rsp["model_version"]
    run = _mk_run(vr["run_id"])

    model_uri = f"models:/{model_name}/{version}"
    model_artifact_path = model_download_utils.get_relative_model_path(vr["source"], vr["run_id"])
    mlflow_model = _dump_mlflow_model.build(model_uri)
    mlflow_model = _mk_mlflow_model(vr, run, mlflow_model) 
    model_summary = _mk_model_summary(vr, run, model_artifact_path, mlflow_model) 

    return {
        "model_summary": model_summary,
        "mlflow_model": mlflow_model,
        "registered_model_version": _mk_version_summary(vr),
        "registered_model": _mk_registered_model(model_name),
        "run": _mk_run_summary(run),
        "experiment": _mk_experiment(run["info"]["experiment_id"])
    }


def _mk_native_flavor_summary(mlflow_model):
    """ 
    Make native flavor summary
    """
    def _prune(flavor):
        """ Remove metadata keys that are not 'data' and do not contain 'version'. """
        flavor2 = flavor.copy()
        for k in flavor.keys():
            if k != "data" and not "version" in k:
                flavor2.pop(k,None)
        return flavor2

    model_info = mlflow_model.get("model_info")
    flavors = model_info.get("_flavors")
    if len(flavors) == 1: # not native flavor, only pyfunc - for feature store flavor
        flavor_name = list(flavors.keys())[0] 
        flavor = flavors.get(flavor_name)
        flavor_summary = { 
            "flavor": flavor_name,
            "loader_module": flavor.get("loader_module")
        }
    elif len(flavors) == 2:
        flavor_names = { k:v for k,v in flavors.items() if k != "python_function" }
        flavor_name = list(flavor_names.keys())[0] # assume there is just one
        flavor = flavors.get(flavor_name)
        flavor_summary = _prune(flavor)
    else:
        flavor_summary = "Internal error"

    return {
        "time_created": model_info.get("_utc_time_created"),
        "native_flavor": flavor_summary,
        "size": mlflow_model.get("model_artifacts_size")
    }


def _mk_model_summary(vr, run, model_artifact_path, mlflow_model):
    """
    Make top-level model summary
    """
    model_info = mlflow_model["model_info"]
    native_flavor = _mk_native_flavor_summary(mlflow_model)
    info = run["info"]
    tags = run["data"]["tags"]
    return {
        "general": {
            "user": report_utils.get_user(run),
            "report_time": ts_now_fmt_utc,
            "model_time_created": model_info.get("_utc_time_created"),
            "tracking_server": str(http_client)
        },
        "registered_model": {
            "name": vr["name"],
            "version": vr["version"],
            "stage": vr["current_stage"]
        },
        "mlflow_model": {
            "model_name": model_artifact_path,
            "run_id": vr["run_id"],
            "run_name": _get_run_name(tags),
            "run_description": _get_run_description(tags),
            "experiment": {
                "name": info["_experiment_name"],
                "experiment_id": info["experiment_id"]
           }
        }, 
        "native_model": native_flavor
    }

def _mk_version_summary(vr):
    """
    Structure the model version summary
    """
    return {
        "name": vr["name"],
        "version": vr["version"],
        "current_stage": vr.get("current_stage"),
        "status": vr.get("status"),
        "aliases": vr.get("aliases"),
        "description": vr.get("description"),
        "tags": mlflow_utils.mk_tags_dict(vr.get("tags",[])),
        "creation_timestamp": fmt_ts_millis(vr.get("creation_timestamp")),
        "last_updated_timestamp": fmt_ts_millis(vr.get("last_updated_timestamp")),
        "mlflow_tracking_server_uri": str(http_client)
    }


def _mk_run(run_id):
    """
    Get and tweak the registered model
    """
    rsp = http_client.get("runs/get", { "run_id": run_id })
    run = rsp["run"]
    return dump_run.build_run(run)


def _mk_run_summary(run):
    """ 
    Tweak run fields for summary purposes 
    """
    run = run.copy()

    info = run["info"]
    tags = run["data"]["tags"]
    info["run_name"] = _get_run_name(tags)
    info["run_description"] = _get_run_description(tags)
    info["start_time"] = info["_start_time"]
    info["end_time"] = info["_end_time"]
    info["duration_seconds"] = info["_duration"]
    info = { ** { "experiment_name": info["_experiment_name"] }, **info }
    to_pop = [ "_start_time", "_end_time", "run_uuid", "_experiment_name", "_duration" ]
    for key in to_pop:
        info.pop(key,None)
    run["info"] = info

    data = run.pop("data",None)
    run["params"] = mlflow_utils.mk_tags_dict(data.get("params",{}))
    run["metrics"] = data.get("metrics",{})
    run["user_tags"] = { k:v for k,v in data.get("tags",{}).items() 
        if not k.startswith("mlflow") and not k == "sparkDatasourceInfo"
    } 
    return run


def _get_run_name(tags):
    return tags.get("mlflow.runName","")

def _get_run_description(tags):
    return tags.get("mlflow.note.content","")


def _mk_mlflow_model_sources(vr):
    """
    Represents a version's two URI sources for MLflow model: the run URI and the 'cached registry' model
    """
    download_uri = http_client.get("model-versions/get-download-uri", {"name": vr["name"], "version": vr["version"] })
    return {
        "run_model_uri": vr.get("source"),
        "registry_model_uri": download_uri.get("artifact_uri")
    }


def _mk_mlflow_model(vr, run, model_info):
    """
    MLflow model details 
    """
    run_id = run["info"]["run_id"]
    model_artifact_path = model_download_utils.get_relative_model_path(vr["source"], run_id)
    model_artifacts = report_utils.build_artifacts(run_id, model_artifact_path)
    return {
        "model_name": model_artifact_path,
        "model_artifacts_size": model_artifacts["summary"]["size"],
        "model_source_uris": _mk_mlflow_model_sources(vr),
        "model_info": model_info["model_info"],
        "model_run_context": _model_run_context(run["data"]["tags"]),
        "model_artifacts": model_artifacts
    }


def _model_run_context(tags):
    """
    Structure a run's 'mlflow' and 'mlflow.databricks' tags
    """
    return {
        "workspace": _get_tags_match(tags, "mlflow.databricks.w"),
        "source_code": _mk_source_code(tags),
        "cluster": _get_tags_match(tags, "mlflow.databricks.cluster"),
        "spark_datasource": _mk_sparkDatasourceInfo(tags)
    }


def _mk_sparkDatasourceInfo(tags):
    """
    Return a list of data sources from undocumented 'sparkDatasourceInfo' tag field.
    """
    return [ v for k,v in tags.items() if k == "sparkDatasourceInfo" ]


def _mk_source_code(tags):
    """
    Structure the various run 'mlflow' tags pointing to the source code
    """
    def _add_tags(dct, tags, prefix):
        matches = _get_tags_match(tags, prefix)
        dct[prefix] = matches
    source_code = {}
    _add_tags(source_code, tags, "mlflow.source")
    _add_tags(source_code, tags, "mlflow.databricks.gitRepo")
    _add_tags(source_code, tags, "mlflow.databricks.notebook")
    return source_code


def _mk_experiment(experiment_id):
    """
    Get and tweak the experiment
    """
    rsp = http_client.get("experiments/get", { "experiment_id": experiment_id })
    exp = rsp["experiment"]
    exp["creation_time"] =  fmt_ts_millis(exp.get("creation_time"))
    exp["last_update_time"] =  fmt_ts_millis(exp.get("last_update_time"))
    exp["tags"] = mlflow_utils.mk_tags_dict(exp.get("tags"))
    exp["description"] =  _get_run_description(exp.get("tags"))
    return exp 


def _mk_registered_model(model_name):
    """
    Get and tweak the registered model
    """
    reg_model = _dump_registered_model.dump(
        model_name,
        artifact_max_level = 0,
        dump_permissions = True,
        silent = True
    )
    reg_model["latest_versions"] = len(reg_model["latest_versions"])
    reg_model["creation_timestamp"] = reg_model["_creation_timestamp"]
    reg_model["last_updated_timestamp"] = reg_model["_last_updated_timestamp"]
    to_pop = [ "_creation_timestamp", "_last_updated_timestamp", "_tracking_uri" ]
    for key in to_pop:
        reg_model.pop(key, None)
    return reg_model


def _get_tags_match(tags, key):
    return { k:v for k,v in tags.items() if k.startswith(key) }


def report(
        model_name, 
        version, 
        show_system_info = False,
        format = "json",
        output_file = None
    ):
    """
    Display and write to file a model version report
    """
    dct = build_report(model_name, version)
    dump_finish(dct, output_file, format, show_system_info, __file__, 
        key = "report_info",
        build_system_info_func = report_utils.build_system_info
    )


@click.command()
@click.option("--model",
     help="Registered model name.",
     type=str,
     required=True
)
@click.option("--version",
     help="Registered model version.",
     type=str,
     required=True
)  
@opt_show_system_info
@opt_format
@opt_output_file

def main(model, version, show_system_info, output_file, format):
    print("Options:")
    for k,v in locals().items():
        print(f"  {k}: {v}")
    report(model, version, show_system_info, format, output_file)


if __name__ == "__main__":
    main() 
