"""
Base class that return MLflow API search results for either classical "list" or "iterator" style using page tokens.
"""

from abc import abstractmethod, ABCMeta


class MlflowApi(metaclass=ABCMeta):

    # List methods

    @abstractmethod
    def search_experiments(self, view_type=None, filter=None):
        pass

    @abstractmethod
    def search_registered_models(self, filter=None):
        pass

    @abstractmethod
    def search_model_versions(self, filter=None):
        pass

    @abstractmethod
    def search_model_versions_by_models(self, filter=None):
        pass

    @abstractmethod
    def search_runs(self, experiment_ids, filter=None, view_type=None):
        pass

    # Count methods

    def count_experiments(self, view_type=None, filter=None):
        return len(self.search_experiments(view_type=view_type, filter=filter))

    def count_registered_models(self, filter=None):
        return len(self.search_registered_models(filter=filter))

    def count_model_versions(self, filter=None):
        return len(self.search_model_versions(filter=filter))

    def count_model_versions_by_models(self, filter=None):
        return len(self.search_model_versions_by_models(filter=filter))
