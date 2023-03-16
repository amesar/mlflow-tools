
from mlflow_tools.client.http_client import DatabricksHttpClient
from mlflow_tools.common import MlflowToolsException

dbx_client = DatabricksHttpClient()


def add_experiment_permissions(experiment_id, dct):
    perm_levels = _call(f"permissions/experiments/{experiment_id}/permissionLevels", "permission_levels")
    perms = _call(f"permissions/experiments/{experiment_id}")
    dct["permissions"] = { **perm_levels, **{ "permissions": perms } }


def add_model_permissions(model_dct):
    model_id = model_dct["id"]
    perm_levels = _call(f"permissions/registered-models/{model_id}/permissionLevels","permission_levels")
    perms = _call(f"permissions/registered-models/{model_id}")
    model_dct["permissions"] = { **perm_levels, **{ "permissions": perms } }


def _call(path, root=None):
    try:
        return dbx_client.get(path)
    except MlflowToolsException as e:
        print("ERROR:",e)
        error = { "error": str(e) }
        if root:
            error = { root: error }
        return error
