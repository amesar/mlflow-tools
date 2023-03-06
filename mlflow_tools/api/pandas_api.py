"""
Return MLflow search method results as a Pandas Dataframe
"""

import pandas as pd
from mlflow.entities import ViewType
from mlflow_tools.api.mlflow_api import MlflowApi
from mlflow_tools.common.timestamp_utils import fmt_ts_millis


class PandasMlflowApi(MlflowApi):

    def __init__(self, mlflow_api):
        self.mlflow_api = mlflow_api

    # Search methods

    def search_experiments(self, view_type=ViewType.ACTIVE_ONLY, filter=None):
        exps = self.mlflow_api.search_experiments(view_type=view_type, filter=filter)
        list = [(exp.experiment_id, 
                 exp.name,
                 fmt_ts_millis(exp.creation_time), 
                 fmt_ts_millis(exp.last_update_time),
                 exp.lifecycle_stage, exp.artifact_location)
             for exp in exps ]
        columns = ["experiment_id", "name", "creation_time", "last_update_time", "lifecycle_stage", "artifact_location"]
        return pd.DataFrame(list, columns=columns)


    def search_registered_models(self, filter=None):
        models = self.mlflow_api.search_registered_models(filter=filter)
        list = [ [ m.name, 
                   len(m.latest_versions),
                   fmt_ts_millis(m.creation_timestamp), 
                   fmt_ts_millis(m.last_updated_timestamp),
                   m.description ] 
            for m in models ]
        columns = ["name", "latest_versions", "creation_timestamp", "last_updated_timestamp", "description" ]
        return pd.DataFrame(list, columns=columns)


    def search_model_versions(self, filter=None):
        versions = self.mlflow_api.search_model_versions(filter=filter)
        return self._versions_to_pandas_df(versions)
        

    def search_model_versions_by_models(self, filter=None):
        models = self.mlflow_api.search_registered_models(filter=filter)
        versions = []
        for m in models:
            _versions = self.mlflow_api.search_model_versions(filter=f"name = '{m.name}'")
            versions += _versions
        return self._versions_to_pandas_df(versions)


    def _versions_to_pandas_df(self, versions):
        lst = [(vr.name,
                vr.version,
                vr.current_stage,
                vr.status,
                fmt_ts_millis(vr.creation_timestamp), 
                fmt_ts_millis(vr.last_updated_timestamp),
                vr.run_id,
                vr.run_link,
                vr.source)
            for vr in versions ]
        columns = ["name", "version", "current_stage", "status", "creation_timestamp", "last_updated_timestamp", "run_id", "run_link", "source" ]
        return pd.DataFrame(lst, columns=columns)


    # Count methods

    def count_experiments(self, view_type=ViewType.ACTIVE_ONLY, filter=None):
        return len(self.mlflow_api.search_experiments(view_type=view_type, filter=filter))


    def count_registered_models(self, filter=None):
        return len(self.mlflow_api.search_registered_models(filter=filter))


    def count_model_versions(self, filter=None):
        return len(self.mlflow_api.search_model_versions(filter=filter))


    def count_model_versions_by_models(self, filter=None):
        return len(self.mlflow_api.search_model_versions_by_models(filter=filter))


    def __repr__(self):
        return str(type(self.mlflow_api))
