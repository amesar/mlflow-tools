# mlflow-tools - Databricks Notebooks


Notebooks to view or manipulate MLflow objects.
See also the [_README.py](_README.py) notebook.

## Overview

**Two sets of notebooks**
* [Display notebooks](display) - view MLflow objects (dump and list), e.g. dump a registered model and its versions in JSON.
* [Tools notebooks](tools) - manipulate MLflow objects, e.g. rename a registered model. 

**Console shell script notebook**
* Shows how to call command line scripts from a notebook shell (%sh) cell.
* [Console_Shell_Scripts](Console_Shell_Scripts.py) notebook.

**Sample notebook screenshots**
  * [List registered models](../samples/databricks_mlflow/notebooks/List_Models.png)
  * [Dump registered model](../samples/databricks_mlflow/notebooks/Dump_Model_01.png)
  and list its [versions](../samples/databricks_mlflow/notebooks/Dump_Model_02.png)


## Load notebooks into Databricks workspace

You can load these notebooks into Databricks either as a workspace folder or a Git Repo.

### Load directory as Databricks workspace folder

See the [Workspace CLI](https://docs.databricks.com/dev-tools/cli/workspace-cli.html).

```
git clone https://github.com/amesar/mlflow-tools

cd mlflow-tools

databricks workspace import_dir 
  databricks_notebooks \
  /Users/me@my.company.com/mlflow-tools
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
    "path": "/Repos/me@my.company.com/mlflow-tools",
    "sparse_checkout": {
      "patterns": [ "databricks_notebooks" ]
      }
    }'
```
