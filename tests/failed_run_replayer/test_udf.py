import pyspark
from pyspark.sql import SparkSession
import pyspark.sql.functions as F

import mlflow
from mlflow_tools.failed_run_replayer import CreateFailedRunReplayer
from tests.utils_test import create_experiment
from . common import train, run_test_no_exception, run_test_raise_mlflow_429_ex_exception, dump
from . common import client, replay_dir, data

spark = SparkSession.builder.appName("App").master("local[2]").getOrCreate()
print("Spark Version:", spark.version)
print("PySpark Version:", pyspark.__version__)

df_data = spark.createDataFrame(data, ["idx"])
#df_data.show(1000,False)

def process(raise_mlflow_429_ex, raise_mlflow_non_429_ex, raise_non_mlflow_ex):
    exp = create_experiment()
    replayer = CreateFailedRunReplayer(replay_dir)
    replayer.remove_files()
    mlflow.set_experiment(exp.name)
    exp = client.get_experiment_by_name(exp.name)

    train_udf = F.udf(train)
    try:
        result = df_data.withColumn("run_id", train_udf(df_data["idx"], 
            F.lit(exp.experiment_id), F.lit(replay_dir), 
            F.lit(True), 
            F.lit(raise_mlflow_429_ex),
            F.lit(raise_mlflow_non_429_ex),
            F.lit(raise_non_mlflow_ex)))
        result.show(1000,False)
        ex = None
    except Exception as e:
        ex = e

    runs = client.list_run_infos(exp.experiment_id)
    return replayer,exp,runs,ex


def test_no_exception():
    run_test_no_exception(process)

def test_raise_mlflow_429_ex_exception():
    run_test_raise_mlflow_429_ex_exception(process)

def test_raise_mlflow_non_429_ex_exception():
    replayer,_,runs,ex = process(False, True, False)
    #dump(replayer)
    assert ex # py4j.protocol.Py4JJavaError
    assert 5 == len(runs)
    failed_runs = replayer.list_run_details()
    assert len(failed_runs) == 0

def test_raise_non_mlflow_ex_exception():
    replayer,_,runs,ex = process(False, False, True)
    assert ex 
    assert 6 == len(runs)
    failed_runs = replayer.list_run_details()
    assert len(failed_runs) == 0
