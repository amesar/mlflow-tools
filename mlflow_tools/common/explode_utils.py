"""
Recursively walk a dict or list and explode JSON string values and the idiosyncratic 'sparkDatasourceInfo' value.
"""

import json

TAG_sparkDatasourceInfo = "sparkDatasourceInfo"


def parse_sparkDatasourceInfo_tag(spec):
    """
    Parses the text value of tag 'sparkDatasourceInfo".
    This is an undocumented system-like tag that does not have an MLflow system prefix 'mlflow.'.
    See https://mlflow.org/docs/latest/tracking.html#system-tags.
    Format is apparently that each data source is separated by a new line.
    Withing a data source, key/values (with '=') are separated by a ','.
    """
    def parse_datasource(spec):
        toks = spec.split(",")
        dct = {}
        for tok in toks:
            k,v = tok.split("=")
            dct[k] = v
        return dct
    toks = spec.split("\n")
    return [ parse_datasource(tok) for tok in toks ]


def _explode_string(v):
    try:
        v2 = json.loads(v)
        if isinstance(v2,dict) or isinstance(v2,list):
            explode_json(v2)
        return v2
    except json.decoder.JSONDecodeError: # not a JSON value 
        return v


def _explode_json_dict(dct):
    if dct.keys() == {"key", "value"} and dct.get("key") == TAG_sparkDatasourceInfo:
        dct["value"] = parse_sparkDatasourceInfo_tag(dct["value"])
    else:
        for k,v in dct.items():
            if isinstance(v,dict) or isinstance(v,list):
                explode_json(v)
            elif isinstance(v,str):
                if k == TAG_sparkDatasourceInfo:
                    dct[k] = parse_sparkDatasourceInfo_tag(v)
                else:
                    dct[k] = _explode_string(v)


def explode_json(obj):
    """
    Recursively walks a dict or list and explodes JSON string values and the idiosyncratic 'sparkDatasourceInfo' value.
    """
    if isinstance(obj, dict):
        _explode_json_dict(obj)
    elif isinstance(obj, list):
        for e in obj:
            explode_json(e)


def main(path):
    from mlflow_tools.common import object_utils
    print("path:",path)
    with open(path, "r", encoding="utf-8") as f:
        dct = json.load(f)
    explode_json(dct)
    object_utils.write_dict_as_json(dct, "out.json")
    object_utils.dump_dict_as_json(dct)
    print("path:",path)


if __name__ == "__main__": 
    import sys
    main(sys.argv[1])
