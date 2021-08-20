
import os
import shutil
import mlflow
from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.ml import Pipeline
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler, StringIndexer
from mlflow_tools.spark.sparkml_udf_workaround import log_udf_model

print("MLflow Tracking URI:", mlflow.get_tracking_uri())
spark_session = SparkSession.builder.appName("app").getOrCreate()

if os.path.exists("mlruns"):
    shutil.rmtree("mlruns")

skip_workaround = os.environ.get("SKIP_WORKAROUND",None)
print("skip_workaround:",skip_workaround)

def test_sparkml_udf():
    model_name = "spark-model"
    features = ["sepal_length", "sepal_width", "petal_length", "petal_width", "species"]
    data_df = spark_session.createDataFrame(
        [
            (5.1, 3.5, 1.4, 0.2, "setosa"),
            (7.0, 3.2, 4.7, 1.4, "versicolor")

        ],
        features
    )
    print("Data:")
    data_df.show()

    feature_cols = data_df.columns[:-1]
    assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")
    indexer = StringIndexer(inputCol="species", outputCol="label")
    clf = DecisionTreeClassifier()
    pipeline = Pipeline(stages=[assembler, indexer, clf])
    model = pipeline.fit(data_df)
    
    with mlflow.start_run() as run:
        mlflow.spark.log_model(model, model_name)
        log_udf_model(run.info.run_id, model_name, data_df.columns)
    
    features.remove("species")
    data_df = data_df.drop("species")

    if not skip_workaround:
        model_name = f"udf-{model_name}"
    model_path = f"runs:/{run.info.run_id}/{model_name}"
    print("model_path:",model_path)
    udf = mlflow.pyfunc.spark_udf(spark=spark_session, model_uri=model_path)
    predictions = data_df.withColumn("prediction", udf(*features))
    print("Predictions:")
    predictions.show()
