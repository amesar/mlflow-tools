"""
Creates a TensorFlow Serving Docker container with an embedded MLflow MLflow Keras TensorFlow 2 model.
Based upon: https://www.tensorflow.org/tfx/serving/docker#creating_your_own_serving_image.
"""

import os
from subprocess import Popen, PIPE
import click
import tensorflow as tf
import mlflow
import mlflow.keras
from mlflow.utils.file_utils import TempDir

client = mlflow.tracking.MlflowClient()

@click.command()
@click.option("--model-uri", help="MLflow Model URI", required=True, type=str)
@click.option("--base-container", help="Base container name", default="tfs_serving_base", type=str)
@click.option("--container", help="Container name", required=True, type=str)
@click.option("--port", help="Port (default is 8502)", default="8502", type=int)
@click.option("--tfs-model-name", help="TensorFlow Serving model name", required=True, type=str)
@click.option("--commands-file", help="Commands file", default=None, type=str)
def main(model_uri, tfs_model_name, base_container, container, port, commands_file):
    print("Options:")
    for k,v in locals().items(): print(f"  {k}: {v}")

    # Extract run ID and artifact path from model URI
    if not model_uri.startswith("runs:/"):
        raise Exception(f"model-uri '{model_uri}' must begin with 'runs:/'")
    run_id, artifact_path = parse_runs_uri(model_uri,"runs")
    print("run_id:",run_id)
    print("artifact_path:",artifact_path)

    # Load the Keras model
    model = mlflow.keras.load_model(model_uri)
    print("model:",type(model))

    local_path = client.download_artifacts(run_id, artifact_path)
    print("local_path:",local_path)

    with TempDir() as tmp:
        savedmodel_path = tmp.path()
        savedmodel_dir = os.path.basename(savedmodel_path)
        print("savedmodel_path:",savedmodel_path)

        # Convert MLflow Keras  model from HD5 into SavedModel format
        tf.keras.models.save_model(model, savedmodel_path, overwrite=True, include_optimizer=True)

        # Setup docker commands
        base_image = "tensorflow/serving"
        commands = [
            f"docker run -d --name {base_container} {base_image}" ,
            f"docker cp {savedmodel_path}/ {base_container}:/tmp",
            f"docker exec -d {base_container} mkdir -p /models/{tfs_model_name}",
            f"docker exec -d {base_container} mv /tmp/{savedmodel_dir} /models/{tfs_model_name}/01",
            f'docker commit --change "ENV MODEL_NAME {tfs_model_name}" {base_container} {container}' ,
            f"docker rm -f {base_container}",
            f"docker run -d --name {container} -p {port}:8501 {container}"
        ]

        # Execute each command individually
        if commands_file:
            with open(commands_file, "w") as fp:
                fp.write("\n")
                for cmd in commands:
                    fp.write(f"{cmd}\n")
            commands_file = os.path.abspath(commands_file)
            run_command(f"sh {commands_file}")
        # Execute all command as one script
        else:
            for cmd in commands:
                run_command(cmd)

def run_command(cmd):
    print("Running command:",cmd)
    proc = Popen(cmd.split(" "), stdout=PIPE, stderr=PIPE, universal_newlines=True)
    proc.wait()
    check_proc(proc, cmd)

def check_proc(proc, cmd):
    if (proc.stderr):
        output = proc.stderr.read()
        if len(output) > 0:
            raise Exception(f"Failed to execute command '{cmd}'. Error: {output}")

def parse_runs_uri(uri, scheme):
    """
    Returns run ID and artifact path from an MLflow runs URI.
    """
    uri = uri.replace(f"{scheme}:/","")
    idx = uri.find("/")
    if idx == -1:
        raise Exception(f"model-uri '{uri}' must be of the form 'runs:/774f1d5e4573499a8eb2043c397cd98a/keras-model'")
    return uri[0:idx], uri[idx+1:]

if __name__ == "__main__":
    main()
