"""
Implements MLflowApi to return search results in "list" style with direct calls to MLflowCient search methods without page tokens.
"""

import mlflow
from mlflow.entities import ViewType
from mlflow_tools.api.mlflow_api import MlflowApi


class SearchMlflowApi(MlflowApi):
    def __init__(self, client=None):
        self.client = client if client else mlflow.client.MlflowClient()


    # List methods

    def search_experiments(self, view_type=ViewType.ACTIVE_ONLY, filter=None):
        return self.client.search_experiments(view_type=view_type, filter_string=filter)

    def search_registered_models(self, filter=None):
        return self.client.search_registered_models(filter_string=filter)

    def search_model_versions(self, filter=None):
        return self.client.search_model_versions(filter_string=filter)

    def search_model_versions_by_models(self, filter=None):
        models = self.client.search_registered_models(filter_string=filter)
        versions = []
        for m in models:
            _versions = self.search_model_versions(filter=f"name = '{m.name}'")
            versions += _versions
        return versions

    def search_runs(self, experiment_ids, filter=None, view_type=None):
        return self.client.search_runs(experiment_ids, filter_string=filter, run_view_type=view_type)


    # Count methods

    def count_model_versions_by_models(self, filter=None):
        models = self.client.search_registered_models(filter_string=filter)
        count = 0
        for m in models:
            _versions = self.search_model_versions(filter=f"name = '{m.name}'")
            count += len(_versions)
        return count
