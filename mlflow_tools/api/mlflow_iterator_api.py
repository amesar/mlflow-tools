"""
Implements MLflowApi to return search results in "iterator" style using page tokens.
"""

import mlflow
from mlflow.entities import ViewType
from mlflow_tools.api.mlflow_api import MlflowApi
from mlflow_tools.common.iterators import (
    SearchExperimentsIterator,
    SearchRegisteredModelsIterator,
    SearchModelVersionsIterator
)


class IteratorMlflowApi(MlflowApi):
    def __init__(self, client=None):
        self.client = client if client else mlflow.client.MlflowClient()

    # List methods

    def search_experiments(self, view_type=ViewType.ACTIVE_ONLY, filter=None):
        return [ exp for exp in SearchExperimentsIterator(self.client, view_type=view_type, filter=filter) ]

    def search_registered_models(self, filter=None):
        return [ m for m in SearchRegisteredModelsIterator(self.client, filter=filter) ]

    def search_model_versions(self, filter=None):
        return [ vr for vr in SearchModelVersionsIterator(self.client, filter=filter) ]


    def search_model_versions_by_models(self, filter=None):
        models = self.search_registered_models(filter=filter)
        versions = []
        for m in models:
            _versions = self.search_model_versions(filter=f"name = '{m.name}'")
            versions += _versions
        return versions


    # Count methods

    # We re-implement the count methods instead of using the default base class implementation,
    # This optimization just materializes one page chunk instead of all page chunks just to count the objects.

    def count_experiments(self, view_type=ViewType.ACTIVE_ONLY, filter=None):
        it = SearchExperimentsIterator(self.client, view_type=view_type, filter=filter)
        return _count_iter(it)

    def count_registered_models(self, filter=None):
        it = SearchRegisteredModelsIterator(self.client, filter=filter)
        return _count_iter(it)

    def count_model_versions(self, filter=None):
        it = SearchModelVersionsIterator(self.client, filter=filter)
        return _count_iter(it)

    def count_model_versions_by_models(self, filter=None):
        it = SearchRegisteredModelsIterator(self.client, filter=filter)
        vr_count=0
        for m in it:
            vr_count += self.count_model_versions(filter=f"name = '{m.name}'")
        return vr_count


def _count_iter(it):
    """ 
    Optimization to just materialize one page chunk instead of all page chunks just to count all objects.
    """ 
    count = 0
    for _ in it:
        count += 1
    return count
