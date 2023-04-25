import os
import getpass
import json
import yaml


def _is_yaml(path, file_type=None):
    return any(path.endswith(x) for x in [".yaml",".yml"]) or file_type in ["yaml","yml"]


def write_file(path, content, file_type=None):
    """
    Write to JSON, YAML or text file.
    """
    #path = _filesystem.mk_local_path(path)
    if path.endswith(".json"):
        with open(path, "w", encoding="utf-8") as f:
            f.write(json.dumps(content, indent=2)+"\n")
    elif _is_yaml(path, file_type):
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(content, f)
    else:
        with open(path, "wb" ) as f:
            f.write(content)


def read_file(path, file_type=None):
    """
    Read a JSON, YAML or text file.
    """
    #with open(_filesystem.mk_local_path(path), "r", encoding="utf-8") as f:
    with open(path, "r", encoding="utf-8") as f:
        if path.endswith(".json"):
            return json.loads(f.read())
        elif _is_yaml(path, file_type):
            return yaml.safe_load(f)
        else:
            return f.read()


