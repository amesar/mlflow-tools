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
from mlflow.tracking.artifact_utils import _download_artifact_from_uri

client = mlflow.tracking.MlflowClient()

@click.command()
@click.option("--model-uri", help="MLflow model URI.", required=True, type=str)
@click.option("--base-container", help="Base container name.", default="tfs_serving_base", type=str)
@click.option("--container", help="Container name.", required=True, type=str)
@click.option("--port", help="Port (default is 8502).", default="8502", type=int)
@click.option("--tfs-model-name", help="TensorFlow Serving model name.", required=True, type=str)
@click.option("--execute-as-commands-file", help="Due to bug, execute all docker commands together in one commands file. Default is True", default=True, type=bool)

def main(model_uri, tfs_model_name, base_container, container, port, execute_as_commands_file):
    print("Options:")
    for k,v in locals().items(): print(f"  {k}: {v}")

    # Load the Keras model
    model = mlflow.keras.load_model(model_uri)
    print("model:",type(model))

    # Download model artifact
    local_path = _download_artifact_from_uri(model_uri)
    print("local_path:",local_path)

    with TempDir() as tmp:
        savedmodel_path = tmp.path()
        savedmodel_dir = os.path.basename(savedmodel_path)
        print("savedmodel_path:",savedmodel_path)

        # Convert MLflow Keras model from HD5 to SavedModel format
        tf.keras.models.save_model(model, savedmodel_path, overwrite=True, include_optimizer=True)

        # Setup docker commands
        base_image = "tensorflow/serving"
        commands = [
            f"docker run -d --name {base_container} {base_image}" ,
            f"docker cp {savedmodel_path}/ {base_container}:/tmp",
            f"docker exec -d {base_container} mkdir -p /models/{tfs_model_name}",
            f"docker exec -d {base_container} mv /tmp/{savedmodel_dir} /models/{tfs_model_name}/01", # 01 is TFS model version
            f'docker commit --change "ENV MODEL_NAME {tfs_model_name}" {base_container} {container}' ,
            f"docker rm -f {base_container}",
            f"docker run -d --name {container} -p {port}:8501 {container}"
        ]

        # Execute each command individually
        if execute_as_commands_file:
            commands_file = "commands.sh"
            with open(commands_file, "w") as fp:
                fp.write("\n")
                for cmd in commands:
                    fp.write(f"{cmd}\n")
            commands_file = os.path.abspath(commands_file)
            run_command(f"sh {commands_file}")
        # Execute all command as one script because docker commit fails mysterioulsy. See README.md.
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

if __name__ == "__main__":
    main()
