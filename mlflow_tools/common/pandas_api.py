"""
Return MLflow search find results as a Pandas Dataframe
"""

import mlflow
from mlflow.entities import ViewType
import pandas as pd
from mlflow_tools.common.iterators import SearchExperimentsIterator
from mlflow_tools.common.iterators import SearchRegisteredModelsIterator
from mlflow_tools.common.iterators import SearchModelVersionsIterator
from mlflow_tools.common.timestamp_utils import fmt_ts_millis

client = mlflow.client.MlflowClient()
print("MLflow Tracking URI:", mlflow.get_tracking_uri())

# List methods

def list_experiments(view_type=ViewType.ACTIVE_ONLY, filter=None):
    exps = [ exp for exp in SearchExperimentsIterator(client, view_type=view_type, filter=filter) ]
    list = [(exp.experiment_id, 
             exp.name,
             fmt_ts_millis(exp.creation_time), 
             fmt_ts_millis(exp.last_update_time),
             exp.lifecycle_stage, exp.artifact_location)
         for exp in exps ]
    columns = ["experiment_id", "name", "creation_time", "last_update_time", "lifecycle_stage", "artifact_location"]
    return pd.DataFrame(list, columns=columns)


def list_models(filter=None):
    models = [ m for m in SearchRegisteredModelsIterator(client, filter=filter) ]
    list = [ [ m.name, 
               len(m.latest_versions),
               fmt_ts_millis(m.creation_timestamp), 
               fmt_ts_millis(m.last_updated_timestamp),
               m.description ] 
        for m in models ]
    columns = ["name", "versions", "creation_timestamp", "last_updated_timestamp", "description" ]
    return pd.DataFrame(list, columns=columns)


def list_model_versions(filter=None):
    versions = [ vr for vr in SearchModelVersionsIterator(client, filter=filter) ]
    list = [(vr.name,
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
    return pd.DataFrame(list, columns=columns)


def list_model_versions_by_models(filter=None):
    it = SearchRegisteredModelsIterator(client, filter=filter)
    df = None
    for m in it:
        _df = list_model_versions(filter=f"name = '{m.name}'")
        print(f"model={m.name} versions={_df.shape[0]}")
        if df is None:
            df = _df
        else:
            df = pd.concat([df, _df], axis=0)
    return df


# Count methods

def count_experiments(view_type=ViewType.ACTIVE_ONLY, filter=None):
    it = SearchExperimentsIterator(client, view_type=view_type, filter=filter)
    return _count_iter(it)


def count_models(filter=None):
    it = SearchRegisteredModelsIterator(client, filter=filter)
    return _count_iter(it)


def count_versions(filter=None):
    it = SearchModelVersionsIterator(client, filter=filter)
    return _count_iter(it)


def count_versions_by_models():
    it = SearchRegisteredModelsIterator(client)
    vr_count=0
    for m in it:
        vr_count += count_versions(filter=f"name = '{m.name}'")
    return vr_count

def _count_iter(it):
    count = 0
    for _ in it:
        count += 1
    return count
