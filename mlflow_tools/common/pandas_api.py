"""
Return MLflow search find results as a Pandas Dataframe
"""

import mlflow
from mlflow.entities import ViewType
import pandas as pd
from mlflow_tools.common.iterators import SearchExperimentsIterator
from mlflow_tools.common.iterators import SearchRegisteredModelsIterator
from mlflow_tools.common.iterators import SearchModelVersionsIterator
from mlflow_tools.tools.utils import format_time

client = mlflow.client.MlflowClient()


def list_experiments(view_type=ViewType.ACTIVE_ONLY, filter=None):
    exps = [ exp for exp in SearchExperimentsIterator(client, view_type=view_type, filter=filter) ]
    list = [(exp.experiment_id, exp.name,
             format_time(exp.creation_time), format_time(exp.last_update_time),
             exp.lifecycle_stage, exp.artifact_location)
         for exp in exps ]
    columns = ["experiment_id", "name", "creation_time", "last_update_time", "lifecycle_stage", "artifact_location"]
    return pd.DataFrame(list, columns=columns)


def list_models(filter=None):
    models = [ m for m in SearchRegisteredModelsIterator(client, filter=filter) ]
    list = [ [ m.name, 
               len(m.latest_versions),
               format_time(m.creation_timestamp), 
               format_time(m.last_updated_timestamp),
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
             format_time(vr.creation_timestamp), 
             format_time(vr.last_updated_timestamp),
             vr.run_id,
             vr.run_link,
             vr.source)
         for vr in versions ]
    columns = ["name", "version", "current_stage", "status", "creation_timestamp", "last_updated_timestamp", "run_id", "run_link", "source" ]
    return pd.DataFrame(list, columns=columns)
