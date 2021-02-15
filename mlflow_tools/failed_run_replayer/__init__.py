"""
Save run details for MLflow rate limited exceptions and replay later.

* Designed for a rate limited MLflow tracking server that is returning an HTTP 429 (Too Many Requests) code.
  * Designed for recoverable errors where you can safely retry and expect to succeed.
* Best suited for UDFs when you create MLflow runs in the UDF and overwhelm the Databricks MLflow tracking server with concurrent requests.
* Upon a 429, saves run details for failed runs.
  * Saves params, metrics, tags, model, (model name, log_model function), artifacts and run name.
  * Run details are saved in a pickle file.
* Replay the saved run details and create MLflow runs.
"""

import os
import shutil
import time
import uuid
import cloudpickle as pickle
import mlflow
from mlflow.entities import Metric, Param, RunTag

class ArtifactDetails():
    def __init__(self, artifact_local_path, artifact_path=""):
        self.artifact_local_path = artifact_local_path
        self.artifact_path = artifact_path
        with open(artifact_local_path,"rb") as f:
            self.artifact_bytes = f.read()
    def __repr__(self):
        return (" ".join(f"{k}={v}" for k,v in self.__dict__.items()))
      
class ModelDetails():
    def __init__(self, model, model_name, log_model_func):
        self.model = model
        self.model_name = model_name
        self.log_model_func = log_model_func
    def __repr__(self):
        return (" ".join(f"{k}={v}" for k,v in self.__dict__.items()))
        
class RunDetails():
    def __init__(self, 
                 exception, 
                 run_name = None,
                 params = {},
                 metrics = {}, 
                 tags = {}, 
                 models = [],
                 artifacts = []):
        self.exception_type = str(type(exception)).replace("<class '","").replace("'>","")
        self.exception_message = str(exception)
        self.run_name = run_name
        self.params = params
        self.metrics = metrics
        self.tags = tags
        self.models = models
        self.artifacts = artifacts

class SaveFailedRunReplayer:  
    @staticmethod        
    def save_run(replay_dir, run_id, run_details):
        """ Save run details as a pickle file """
        os.makedirs(replay_dir, exist_ok=True)
        
        # If run was created, delete it since it is in an incomplete state.
        # If call fails in mlflow.start_run we won't be inside a run.
        if run_id:
            print("Deleting failed run_id:",run_id)
            mlflow.tracking.MlflowClient().delete_run(run_id)
                    
        # Save run details as a pickle file for later replay                      
        path = os.path.join(replay_dir, f"{(uuid.uuid4())}.pkl")
        with open(path,"wb") as f:
            pickle.dump(run_details, f)


class CreateFailedRunReplayer:
   
    def __init__(self, replay_dir,do_tag=True):
        self.replay_dir = replay_dir
        self.do_tag = do_tag
        os.makedirs(replay_dir, exist_ok=True)   
            
    def _create_run(self, run):
        args = {"run_name": run.run_name } if run.run_name else {} 
        with mlflow.start_run(**args) as active_run:
            params = [ Param(k,v) for k,v in run.params.items() ] 
            metrics = [ Metric(k,v,int(time.time()),0) for k,v in run.metrics.items() ] # TODO: timestamp and step?
            tags = [ RunTag(k,v) for k,v in run.tags.items() ]
            mlflow.tracking.MlflowClient().log_batch(active_run.info.run_id, metrics, params, tags)
            if self.do_tag:
                mlflow.set_tag("replayed","true")
            for m in run.models:
                if m.model:
                    m.log_model_func(m.model, m.model_name)
            for a in run.artifacts:
                if a.artifact_local_path:
                    if a.artifact_local_path:
                        with open(a.artifact_local_path, "wb") as f:
                            f.write(a.artifact_bytes)
                    mlflow.log_artifact(a.artifact_local_path, a.artifact_path)
            return active_run.info.run_id
        
    def create_runs(self):
        """ Create MLflow runs from pickle file"""
        run_ids = [ self._create_run(run) for run in self.list_run_details() ]
        return run_ids
      
    def list_run_details(self):
        runs = []
        for file in os.listdir(self.replay_dir):
            with open(os.path.join(self.replay_dir,file), "rb") as f:
                runs.append(pickle.load(f))
        return runs
    
    def remove_files(self):
        shutil.rmtree(self.replay_dir)
        os.makedirs(self.replay_dir)
