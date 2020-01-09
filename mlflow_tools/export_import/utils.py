import os
import shutil
import zipfile
import json
import time
import mlflow
from . import mk_local_path

PREFIX_METADATA = "mlflow_tools.metadata"
PREFIX_SRC_RUN = "mlflow_tools.source_run"

# Databricks tags that cannot be set
dbx_skip_tags = set([ "mlflow.user" ])

def create_tags_for_metadata(src_client, run, export_metadata_tags):
    """ Create destination tags from source run """
    tags = run.data.tags.copy()
    for k in dbx_skip_tags:
        tags.pop(k, None)
    if export_metadata_tags:
        uri = mlflow.tracking.get_tracking_uri()
        tags[PREFIX_METADATA+".tracking_uri"] = uri
        dbx_host = os.environ.get("DATABRICKS_HOST",None)
        if dbx_host is not None:
            tags[PREFIX_METADATA+".DATABRICKS_HOST"] = dbx_host
        now = int(time.time()+.5)
        snow = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(now))
        tags[PREFIX_METADATA+".timestamp"] = str(now)
        tags[PREFIX_METADATA+".timestamp_nice"] = snow
        tags[PREFIX_METADATA+".user_id"] = run.info.user_id
        tags[PREFIX_METADATA+".run_id"] =  str(run.info.run_id)
        tags[PREFIX_METADATA+".experiment_id"] = run.info.experiment_id
        exp = src_client.get_experiment(run.info.experiment_id)
        tags[PREFIX_METADATA+".experiment_name"] = exp.name
    tags = { k:v for k,v in sorted(tags.items()) }
    return tags

def create_tags_for_mlflow_tags(tags_dct, import_mlflow_tags):
    from mlflow.entities import RunTag
    tags = []
    for k,v in tags_dct.items() :
        if not import_mlflow_tags and k.startswith("mlflow."): k = PREFIX_SRC_RUN + "."+k
        tags.append(RunTag(k,str(v)))
    return tags

def set_dst_user_id(tags,user_id, use_src_user_id):
    from mlflow.entities import RunTag
    from mlflow.utils.mlflow_tags import MLFLOW_USER
    user_id = user_id if use_src_user_id else get_user_id()
    tags.append(RunTag(MLFLOW_USER,user_id ))

def get_now_nice():
    now = int(time.time()+.5)
    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(now))

def strip_underscores(obj):
    return { k[1:]:v for (k,v) in obj.__dict__.items() }

def write_json_file(fs, path, dct):
    fs.write(path, json.dumps(dct,indent=2)+"\n")

def write_file(path, content):
    with open(mk_local_path(path), 'wb') as f:
        f.write(content)

def read_json_file(path):
    with open(mk_local_path(path), "r") as f:
        return json.loads(f.read())

def zip_directory(zip_file, dir):
    zipf = zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(dir):
        for file in files:
            full_path = os.path.join(root, file)
            relative_path = full_path.replace(dir+"/","")
            zipf.write(full_path,relative_path)
    zipf.close()

def unzip_directory(zip_file, exp_name, funk):
    import tempfile
    temp_dir = tempfile.mkdtemp()
    try:
        with zipfile.ZipFile(zip_file, "r") as f:
            f.extractall(temp_dir)
        funk(exp_name, temp_dir)
    finally:
        shutil.rmtree(temp_dir)

def string_to_list(list_as_string):
    lst = list_as_string.split(",")
    if "" in lst: list.remove("")
    return lst

def get_user_id():
    from mlflow.tracking.context.default_context import _get_user
    return _get_user()
