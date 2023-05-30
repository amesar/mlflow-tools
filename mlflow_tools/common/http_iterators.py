from mlflow.store.entities.paged_list import PagedList

class BaseIterator():
    """
    Base class to iterate for 'search' methods that return PageList.
    """
    def __init__(self, client, resource, max_results=None, filter=None, http_method=None, filter_field_name="filter_string"):
        self.client = client
        self.resource = resource
        self.filter = filter
        self.idx = 0
        self.paged_list = None
        self.kwargs = {}
        if filter: self.kwargs[filter_field_name] = filter
        if max_results: self.kwargs["max_results"] = max_results
        self.http_method = http_method

    def _call_iter(self):
        return self._invoke()

    def _call_next(self):
        return self._invoke(self.paged_list.token)

    def _invoke(self, token=None):
        params = {}
        params = self.kwargs.copy()
        if token: params["page_token"] = token

        if self.http_method and self.http_method.upper() == "POST": # NOTE!!: https://github.com/mlflow/mlflow/issues/7949
            rsp = self.client.post(f"{self.resource}/search", params)
        else:
            rsp = self.client.get(f"{self.resource}/search", params)

        res = rsp
        resource = self.resource.replace("-","_")
        objects = res.get(resource,[])
        next_page_token = res.get("next_page_token")
        return PagedList(objects, next_page_token)


    def __iter__(self):
        self.paged_list = self._call_iter()
        return self

    def __next__(self):
        if self.idx < len(self.paged_list):
            chunk = self.paged_list[self.idx]
            self.idx += 1
            return chunk
        elif self.paged_list.token is None or self.paged_list.token == "":
            raise StopIteration
        else:
            self.paged_list = self._call_next()
            if len(self.paged_list) == 0:
                raise StopIteration
            self.idx = 1
            return self.paged_list[0]


class SearchExperimentsIterator(BaseIterator):
    """
    Usage:
        experiments = SearchExperimentsIterator(client, max_results)
        for experiment in experiments:
            print(experiment)
    """
# TODO: max_results default required bug
    def __init__(self, client, view_type=None, max_results=None, filter=None):
        super().__init__(client,"experiments", max_results=max_results, filter=filter)
        if view_type:
            self.kwargs["view_type"] = view_type


class SearchRegisteredModelsIterator(BaseIterator):
    """
    Usage:
        models = SearchRegisteredModelsIterator(client, max_results)
        for model in models:
            print(model)
    """
    def __init__(self, client, max_results=None, filter=None):
        super().__init__(client,"registered-models", max_results=max_results, filter=filter, filter_field_name="filter")


class SearchModelVersionsIterator(BaseIterator):
    """
    Usage:
        versions = SearchModelVersionsIterator(client)
        for vr in versions:
            print(vr)
    """
    def __init__(self, client, max_results=None, filter=None):
        super().__init__(client,"model-versions", max_results=max_results, filter=filter)


class SearchRunsIterator(BaseIterator):
    def __init__(self, client, experiment_ids, max_results=None, filter=None, view_type=None):
        super().__init__(client, "runs", max_results=max_results, filter=filter, http_method="POST")
        if isinstance(experiment_ids,str):
            experiment_ids = [ experiment_ids ]
        self.kwargs["experiment_ids"] = experiment_ids
        if view_type: 
            self.kwargs["run_view_type"] = view_type
