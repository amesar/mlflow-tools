"""
Dump a registered model version in JSON or YAML.
"""

import click
from mlflow_tools.client.http_client import MlflowHttpClient
from mlflow_tools.common import model_download_utils
from mlflow_tools.common.click_options import (
    opt_artifact_max_level,
    opt_show_tags_as_dict,
    opt_explode_json_string,
    opt_dump_permissions,
    opt_show_system_info,
    opt_format,
    opt_output_file
)
from mlflow_tools.display import dump_run as _dump_run
from mlflow_tools.display import dump_registered_model as _dump_registered_model
from mlflow_tools.display.dump_experiment import adjust_experiment
from mlflow_tools.display.display_utils import build_artifacts
from mlflow_tools.display.display_utils import dump_finish
from mlflow_tools.display.display_utils import adjust_model_version

http_client = MlflowHttpClient()


def dump(
        model_name,
        version,
        dump_run = False,
        dump_run_model = False,
        dump_experiment = False,
        dump_registered_model = False,
        artifact_max_level = 1,
        show_tags_as_dict = True,
        explode_json_string = True,
        dump_permissions = False,
        show_system_info = False,
        format = "json",
        output_file = None
    ):
    rsp = http_client.get("model-versions/get", { "name": model_name, "version": version })

    vr = rsp["model_version"]
    adjust_model_version(http_client, vr, show_tags_as_dict)

    dct = {
      "model_version": vr
    }

    if dump_registered_model:
        reg_model = _dump_registered_model.dump(
            vr["name"],
            artifact_max_level = 0,
            explode_json_string  =  explode_json_string,
            show_tags_as_dict = show_tags_as_dict,
            dump_permissions = dump_permissions,
            silent = True
        )
        reg_model["latest_versions"] = len(reg_model["latest_versions"])
        dct["registered_model"] = reg_model

    run = None
    if dump_run_model:
        rsp = http_client.get("runs/get", { "run_id": vr["run_id"] })
        run = rsp["run"]
        info = run["info"]
        path = model_download_utils.get_relative_model_path(vr["source"], info["run_id"])
        artifacts = build_artifacts(info["run_id"], path, artifact_max_level)
        dct["mlflow_model_artifacts"] = {
            "summary": artifacts.get("summary"),
            "artifacts": artifacts.get("files")
        }

    if dump_run:
        if not run:
            rsp = http_client.get("runs/get", { "run_id": vr["run_id"] })
            run = rsp["run"]
        run = _dump_run.build_run_extended(
                   run = run,
                   artifact_max_level = artifact_max_level,
                   explode_json_string = explode_json_string,
                   show_tags_as_dict = show_tags_as_dict
        )
        dct["run"] = run
        if dump_experiment:
            run = run["run"]
            rsp = http_client.get("experiments/get", { "experiment_id": run["info"]["experiment_id"] })
            exp = rsp["experiment"]
            adjust_experiment(exp, show_tags_as_dict)
            dct["experiment"] = exp

    dct = dump_finish(dct, output_file, format, show_system_info, __file__)


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
@click.option("--dump-run-model",
    help="Dump the run model backing the version.",
    type=bool,
    default=False,
    show_default=True
)
@click.option("--dump-run",
    help="Dump a version's run details.",
    type=bool,
    default=False,
    show_default=True
)
@opt_artifact_max_level
@click.option("--dump-experiment",
    help="Dump the run's experiment.",
    type=bool,
    default=False,
    show_default=True
)
@click.option("--dump-registered-model",
    help="Dump a version's registered model (without version list details).",
    type=bool,
    default=False,
    show_default=True
)
@opt_dump_permissions
@opt_show_tags_as_dict
@opt_explode_json_string
@opt_show_system_info
@opt_format
@opt_output_file

def main(model, version, 
        dump_run, 
        dump_run_model, 
        dump_experiment,
        dump_registered_model,
        artifact_max_level, show_tags_as_dict, explode_json_string,
        dump_permissions,
        show_system_info,
        format,
        output_file
    ):
    print("Options:")
    for k,v in locals().items(): print(f"  {k}: {v}")
    dump(model, version, 
        dump_run, 
        dump_run_model, 
        dump_experiment,
        dump_registered_model,
        artifact_max_level,
        show_tags_as_dict,
        explode_json_string,
        dump_permissions,
        show_system_info,
        format,
        output_file
    )


if __name__ == "__main__":
    main()
