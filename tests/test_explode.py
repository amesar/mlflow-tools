"""
Test explode_utils.py
"""

import copy
import json
from mlflow_tools.display.explode_utils import explode_json
#from mlflow_tools.common.object_utils import dump_dict_as_json

# =====

dct_simple = {
    "name": "foo",
    "address": ' { "street": "main", "city": "Arica" } ',
}

def test_dict():
    dct = dct_simple
    assert isinstance(dct.get("address"),str)
    explode_json(dct)
    #dump_dict_as_json(dct)
    address = dct.get("address")
    assert address 
    assert address.get("street") == "main"
    assert address.get("city") == "Arica"


# =====

lst_key_value_list = [
    { "key": "foo",
      "value": ' { "street": "main", "city": "Arica" } '  }
]

def test_key_value_list():
    lst = lst_key_value_list
    explode_json(lst)
    #dump_dict_as_json(lst)
    address = lst[0].get("value")
    assert address.get("street") == "main"
    assert address.get("city") == "Arica"


# =====

def test_file():
    path = "data/Sklearn_Wine_input_nb.json"
    with open(path, "r",  encoding="utf-8") as f:
        run1 = json.load(f)
    run2 = copy.deepcopy(run1)
    explode_json(run2)
    #dump_dict_as_json(run2)
    assert run1 != run2

    # run.data.tags
    tags1, tags2 = run1["data"]["tags"], run2["data"]["tags"]
    assert tags1 != tags2
    assert_list_same(tags1, tags2, "mlflow.databricks.workspaceURL")
    assert_list_different(tags1, tags2, "mlflow.databricks.cluster.info", dict)
    assert_list_different(tags1, tags2, "mlflow.databricks.cluster.libraries", dict)
    assert_list_different(tags1, tags2, "mlflow.log-model.history", list)
    assert_list_different(tags1, tags2, "sparkDatasourceInfo", list)

    # run.inputs.dataset_inputs.dataset
    inputs1, inputs2 = run1["inputs"], run2["inputs"]
    assert inputs1 != inputs2
    ds_inputs1, ds_inputs2 = inputs1["dataset_inputs"], inputs2["dataset_inputs"]
    assert ds_inputs1 != ds_inputs2
    ds1, ds2 = ds_inputs1[0], ds_inputs2[0]
    assert ds1 != ds2
    ds1, ds2 = ds1["dataset"], ds2["dataset"]
    assert_dict_different(ds1, ds2, "source")
    assert_dict_different(ds1, ds2, "schema")
    assert_dict_different(ds1, ds2, "profile")

def _find_key(lst, key):
    matches = [ x["value"] for x in lst if x["key"] == key ]
    assert len(matches) == 1
    return matches[0]

def assert_dict_different(dct1, dct2, key, dtype=dict):
    v1 = dct1.get(key)
    v2 = dct2.get(key)
    assert isinstance(v1, str)
    assert isinstance(v2, dtype)

def assert_list_different(tags1, tags2, key, dtype):
    v1 = _find_key(tags1,key)
    v2 = _find_key(tags2,key)
    assert isinstance(v1, str)
    assert isinstance(v2, dtype)

def assert_list_same(tags1, tags2, key):
    v1 = _find_key(tags1,key)
    v2 = _find_key(tags2,key)
    assert v1 == v2
