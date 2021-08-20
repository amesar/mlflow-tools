# mlflow-tools tests

## Setup

```
conda env create conda.yaml
source activate mlflow-tools-tests
```
  
## Run tests
```
find . -name "test*.py" | grep -v spark | pytest -s -v
```

## Run Spark tests

```
pip install pyarrow
pip install pyspark==3.1.1

py.test  -s -v spark/test_sparkml_udf_workaround.py
```
