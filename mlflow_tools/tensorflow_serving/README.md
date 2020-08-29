# Serve MLflow Keras model with TensorFlow Serving

Creates a [TensorFlow Serving](https://www.tensorflow.org/tfx/guide/serving) Docker container with an embedded MLflow Keras TensorFlow 2 model.

## Overview

**Summary**
* Based upon TensorFlow documentation [Creating your own serving image](https://www.tensorflow.org/tfx/serving/docker#creating_your_own_serving_image).
* Source code: [launch_tensorflow_serving.py](launch_tensorflow_serving.py).

**Basic steps**
* First create an MLflow Keras TensorFlow 2 model which will be in HD5 format.
* Convert the HD5 model to SavedModel format.
* Create and launch a TensorFlow Serving container with the SavedModel model.
* Score against the container.

**Notes**
* TensorFlow Serving requires models to be in the [SavedModel](https://www.tensorflow.org/guide/saved_model) format.
  * SavedModel (Protobuf based) is the default model format for Keras TensorFlow 2.
  * TensorFlow Serving cannot serve models stored in the legacy HD5 format of Keras TensorFlow 1.
* MLflow currently can only log a Keras model in the HD5 format. See issues:
  * [3224](https://github.com/mlflow/mlflow/issues/3224) - `[BUG] Cannot save Keras/TF_2.x model as SavedModel format using mlflow.keras.log_model with kwargs { "save_format": "tf" }`.
  * [3246](https://github.com/mlflow/mlflow/issues/3246) - `[FR] Serialization format for TensorFlow 2.x (Keras) model should be SavedModel per TF 2.0 doc`.
* MNIST dataset to score is in TensorFlow Serving JSON format. See [data/mnist.json](data/mnist.json).


## TODO

* Fix issue 3246 so Keras models are logged as SavedModel flavor.
* Promote this solution into issue 3303.
* Fix `docker commit` bug. See below.

## Setup

1. Install docker on your machine.

2. Create an MLflow Keras TensorFlow run. Note that it will be in the HD5 format.
You can use the [keras_tf_mnist](https://github.com/amesar/mlflow-examples/tree/master/python/keras_tf_mnist#training) example.

3. Create and activate your conda environment.
```
conda env create conda.yaml
conda activate mlflow-tensorflow-serving
```


## Options

```
python launch_tensorflow_serving.py --help
```

```
Options:
  --model-uri TEXT       MLflow model URI.  [required]
  --base-container TEXT  Base container name.
  --container TEXT       Container name.  [required]
  --port INTEGER         Port (default is 8502).
  --tfs-model-name TEXT  TensorFlow Serving model name.  [required]
  --execute-as-commands-file BOOLEAN
                                  Due to bug, execute all docker commands
                                  together in one commands file. Default is
                                  True
```

The `model-uri` option can be either a `runs` or `models` URI such as:
* runs:/774f1d5e4573499a8eb2043c397cd98a/keras-model
* models:/keras_wine/production
* models:/keras_wine/1

## Run

```
python launch_tensorflow_serving.py \
  --model-uri runs:/774f1d5e4573499a8eb2043c397cd98a/keras-model \
  --tfs-model-name keras_mnist
  --container tfs_serving_keras_mnist
```

### Bug

When running the docker commands individually with Popen (--execute-as-commands-file False), `docker commit` fails mysterioulsy with the following error.

```
Failed to execute command 'docker commit --change "ENV MODEL_NAME keras_mnist" tfs_serving_base tfs_serving_keras_mnist'. Error: "docker commit" requires at least 1 and at most 2 arguments.
```

When all docker commands are run in one script with Popen, no error occurs.

Therefore, the current workaround is to collect all the docker commands into a `docker_commands` file (_commands.sh) and execute this file with one Popen call.


#### Docker commands file example
```
docker run -d --name tfs_serving_base tensorflow/serving
docker cp /var/folders/rp/88lfxw2n4lvgkdk9xl0lkqjr0000gp/T/tmpf2k0n9ti/ tfs_serving_base:/tmp
docker exec -d tfs_serving_base mkdir -p /models/keras_mnist
docker exec -d tfs_serving_base mv /tmp/tmpf2k0n9ti /models/keras_mnist/01
docker commit --change "ENV MODEL_NAME keras_mnist" tfs_serving_base tfs_serving_keras_mnist
docker rm -f tfs_serving_base
docker run -d --name tfs_serving_keras_mnist -p 8502:8501 tfs_serving_keras_mnist
```

## Score

### Score TensorFlow Serving JSON file

```
curl -X POST \
  -d @data/mnist.json \
  http://localhost:8502/v1/models/keras_mnist:predict
```
```
{
  "predictions": [
    [
      3.12299653e-06,
      2.60791438e-07,
      0.000399814453,
      0.000576042803,
      3.31057066e-08,
      1.12317866e-05,
      1.57459468e-09,
      0.998985946,
      9.80186451e-06,
      1.3647702e-05
    ],
. . .
}
```
### Score MNIST PNG file

We first convert the PNG file to JSON format.

```
python convert_png_to_tfs_json.py data/0_9993.png | \
curl -X POST \
  -d @- \
  http://localhost:8502/v1/models/keras_mnist:predict
```
```
{
  "predictions": [[1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
}
```

