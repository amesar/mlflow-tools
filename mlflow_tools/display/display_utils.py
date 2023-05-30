"""
Display utilities.
"""

import os
from dataclasses import dataclass
import getpass
from mlflow_tools.client.http_client import MlflowHttpClient
from mlflow_tools.common.timestamp_utils import ts_now_fmt_utc

http_client = MlflowHttpClient()


def build_system_info(script):
    import mlflow
    import platform
    return {
        "script": os.path.basename(script),
        "display_time": ts_now_fmt_utc,
        "mlflow": {
            "version": mlflow.__version__,
            "tracking_uri": mlflow.get_tracking_uri(),
        },
        "platform": {
            "python_version": platform.python_version(),
            "system": platform.system()
        },
        "user": getpass.getuser(),
    }


def process_df(df, columns=None, sort_attr="name", sort_order="asc", csv_file=None):
    if columns:
        df = df[columns]
    if sort_attr in df.columns:
        df.sort_values(by=[sort_attr], inplace=True, ascending=sort_order == "asc")
    if csv_file:
        with open(csv_file, "w", encoding="utf-8") as f:
            df.to_csv(f, index=False)
    return df


def build_artifacts(run_id, path, artifact_max_level, level=0):
    """
    Build recursive tree of calls to 'artifacts/list' API endpoint.
    :param run_id: Run ID.
    :param path: Relative artifact path.
    :param artifact_max_level: Levels to recurse.
    :return: Nested dict with list of artifacts representing tree node info.
    """
    res = _build_artifacts(run_id, path, artifact_max_level, level)
    summary = {
        "artifact_max_level": artifact_max_level,
        "num_artifacts": res.num_artifacts,
        "num_bytes": res.num_bytes,
        "num_levels": res.num_levels
    } 
    return { **{ "summary": summary }, **res.artifacts }

def _build_artifacts(run_id, path, artifact_max_level, level=0):
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
    if level > artifact_max_level:
        return Result(artifacts, 0, 0, level)

    files = artifacts.get("files", None)
    level += 1
    new_level = level
    num_bytes, num_artifacts = (0,0)
    if files:
        for _,artifact in enumerate(files):
            num_bytes += int(artifact.get("file_size",0)) or 0
            if artifact["is_dir"]:
                res = _build_artifacts(run_id, artifact["path"], artifact_max_level, level)
                if res.num_levels > new_level:
                    new_level = res.num_levels
                num_bytes += res.num_bytes
                num_artifacts += res.num_artifacts
                artifact["artifacts"] = res.artifacts
            else:
                num_artifacts += 1
    return Result(artifacts, num_bytes, num_artifacts, new_level)


def dump_finish(dct, output_file, format, show_system_info, script_name, silent=False):
    from mlflow_tools.display import dump_dct, write_dct
    if show_system_info:
        dct = { **{ "system": build_system_info(script_name)}, **dct }
    if not silent:
        dump_dct(dct, format)
    if output_file and len(output_file) > 0:
        write_dct(dct, output_file, format)
    return dct


def adjust_model_version(http_client, vr, show_tags_as_dict=False):

    # Get 'cached model' registry link
    from mlflow_tools.common import mlflow_utils
    uri = http_client.get("model-versions/get-download-uri", {"name": vr["name"], "version": vr["version"] })
    vr["_download_uri"] = uri

    # Add formatted timestamps
    adjust_model_version_timestamp(vr)

    # Show tags as key/value dictionary
    if show_tags_as_dict:
        v = vr.get("tags")
        if v:
            vr["tags"] = mlflow_utils.mk_tags_dict(v)


def adjust_model_version_timestamp(vr):
    format_ts(vr, "creation_timestamp")
    format_ts(vr, "last_updated_timestamp")


def format_ts(dct, key):
    from mlflow_tools.common.timestamp_utils import fmt_ts_millis
    ts = dct.get(key)
    if ts:
        dct[f"_{key}"] = fmt_ts_millis(int(ts))
