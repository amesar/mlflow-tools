# MLflow Display Objects - Databricks Notebooks

Notebooks to dump or list MLflow objects. See [_README.py](_README.py) for details.

You can load these notebooks into Databricks either as a workspace folder or a Git Repo.

Samples notebook screenshots:
  * [List registered models](../../samples/databricks_mlflow/notebooks/List_Models.png)
  * [Dump registered model](../../samples/databricks_mlflow/notebooks/Dump_Model_01.png)
  and list its [versions](../../samples/databricks_mlflow/notebooks/Dump_Model_02.png)



### Load directory as Databricks workspace folder

See the [Workspace CLI](https://docs.databricks.com/dev-tools/cli/workspace-cli.html).

```
git clone https://github.com/amesar/mlflow-tools

cd mlflow-tools/databricks_notebooks

databricks workspace import_dir 
  display \
  /Users/me@my.company.com/mlflow-tools-display
```

### Clone directory as Databricks Git Repo

You can load a Git Repo either through the Databricks UI or via the command line.

#### 1. Load through Databricks UI

See [Clone a Git Repo & other common Git operations](https://docs.databricks.com/repos/git-operations-with-repos.html).

#### 2. Load from command line with curl

Note it's best to use the curl version since the CLI doesn't appear to support the sparse checkout option.

```
curl \
  https://my.company.com/api/2.0/repos \
  -H "Authorization: Bearer MY_TOKEN" \
  -X POST \
  -d ' {
    "url": "https://github.com/amesar/mlflow-tools",
    "provider": "gitHub",
    "path": "/Repos/me@my.company.com/mlflow-tools-display",
    "sparse_checkout": {
      "patterns": [ "databricks_notebooks/display" ]
      }
    }'
```
