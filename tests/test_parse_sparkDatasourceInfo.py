
from mlflow_tools.common.mlflow_utils import parse_sparkDatasourceInfo_tag

expected2 = set([ "path", "format"])
expected3 = set([ 'path', 'version', 'format'])


def test_one_file():
    v = "path=dbfs:/user/hive/warehouse/andre.db/wine_quality,version=0,format=delta"
    lst  = parse_sparkDatasourceInfo_tag(v)
    assert len(lst) == 1
    print("datasource:",lst[0])
    keys = lst[0].keys()
    print("keys:",keys)
    assert keys == expected3


def test_three_files():
    v = """path=dbfs:/databricks-datasets/wine-quality/winequality-white.csv,format=text
path=dbfs:/databricks-datasets/wine-quality/winequality-white.csv,format=csv
path=dbfs:/databricks-datasets/wine-quality/winequality-red.csv,format=text"""
    lst = parse_sparkDatasourceInfo_tag(v)
    assert len(lst) == 3
    for src in lst:
        print("  datasource:",src)
        assert src.keys() == expected2

def test_mixed():
    v = """path=dbfs:/databricks-datasets/wine-quality/winequality-white.csv,format=text
path=dbfs:/databricks-datasets/wine-quality/winequality-white.csv,format=csv
path=dbfs:/databricks-datasets/wine-quality/winequality-red.csv,format=text
path=dbfs:/user/hive/warehouse/andre.db/wine_quality,version=0,format=delta"""
    lst = parse_sparkDatasourceInfo_tag(v)
    assert len(lst) == 4
    for src in lst:
        print("  datasource:",src)
        if len(src) == 2:
            assert src.keys() == expected2
        elif len(src) == 3:
            assert src.keys() == expected3
        else:
            assert False
