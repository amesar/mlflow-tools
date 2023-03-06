
from mlflow_tools.api.mlflow_iterator_api import IteratorMlflowApi
from mlflow_tools.api.mlflow_list_api import ListMlflowApi
from mlflow_tools.api.pandas_api import PandasMlflowApi

MLFLOW_API_ITERATOR = "iterator"
MLFLOW_API_SEARCH = "list"
DEFAULT_MLFLOW_API = MLFLOW_API_ITERATOR


_mlflow_api_impls = {
  MLFLOW_API_ITERATOR: IteratorMlflowApi(),
  MLFLOW_API_SEARCH: ListMlflowApi()
}


def get_mlflow_api(mlflow_api=DEFAULT_MLFLOW_API):
    impl = _mlflow_api_impls.get(mlflow_api, None)
    if impl is None:
        print(f"WARNING: Illegal value '{mlflow_api}' for PandasMlflowApi implmentation. Legal values are: {MLFLOW_API_ITERATOR}|{MLFLOW_API_SEARCH}. Using default '{DEFAULT_MLFLOW_API}'.")
        impl = _mlflow_api_impls[DEFAULT_MLFLOW_API]
    return impl


def get_pandas_api(mlflow_api=DEFAULT_MLFLOW_API):
    return PandasMlflowApi(get_mlflow_api(mlflow_api))
