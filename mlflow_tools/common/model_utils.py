import time
from mlflow.exceptions import RestException
from mlflow.entities.model_registry.model_version_status import ModelVersionStatus


def delete_model(client, model_name):
    """ Delete a model and all its versions. """
    versions = client.search_model_versions(f"name='{model_name}'") # TODO: handle page token
    print(f"Deleting {len(versions)} versions for model '{model_name}'")
    for vr in versions:
        print(f"Deleting version={vr.version} stage={vr.current_stage} status={vr.status} run_id={vr.run_id}")
        if vr.current_stage != "Archived": # NOTE: for Databricks though OSS works
            client.transition_model_version_stage (model_name, vr.version, "Archived")
        client.delete_model_version(model_name, vr.version)
    client.delete_registered_model(model_name)


def wait_until_version_is_ready(client, model_name, model_version, sleep_time=1, iterations=100):
    """ For Databricks. Due to blob eventual consistency, wait until a newly created version is in READY state. """
    start = time.time()
    for _ in range(iterations):
        vr = client.get_model_version(model_name, model_version.version)
        status = ModelVersionStatus.from_string(vr.status)
        print(f"Version: id={vr.version} status={vr.status} state={vr.current_stage}")
        if status == ModelVersionStatus.READY:
            break
        time.sleep(sleep_time)
    end = time.time()
    print(f"Waited {round(end-start,2)} seconds")
