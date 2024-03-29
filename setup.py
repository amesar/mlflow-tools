from setuptools import setup, find_packages

setup(
    name="mlflow_tools",
    version="1.0.0",
    author="Andre Mesarovic",
    description="MLflow Tools",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    url="https://github.com/amesar/mlflow-tools",
    project_urls={
        "Bug Tracker": "https://github.com/amesar/mlflow-tools/issues",
        "Documentation": "https://github.com/amesar/mlflow-tools/",
        "Source Code": "https://github.com/amesar/mlflow-tools/"
    },
    python_requires = ">=3.8",
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        "mlflow-skinny>=2.2.2",
        "pandas>=1.5.3",
        "wheel",
        "checksumdir"
    ],
    license = "Apache License 2.0",
    keywords = "mlflow ml ai",
    classifiers = [
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent"
    ],
    entry_points = {
        "console_scripts": [
            "count-objects = mlflow_tools.display.count_objects:main",
            "list-experiments = mlflow_tools.display.list_experiments:main",
            "list-models = mlflow_tools.display.list_registered_models:main",
            "list-registered-models = mlflow_tools.display.list_registered_models:main",
            "list-model-versions = mlflow_tools.display.list_model_versions:main",
            "list-model-versions-with-runs = mlflow_tools.display.list_model_versions_with_runs:main",
            "list-runs = mlflow_tools.display.list_runs:main",
            "dump-run = mlflow_tools.display.dump_run:main",
            "dump-experiment = mlflow_tools.display.dump_experiment:main",
            "dump-registered-model = mlflow_tools.display.dump_registered_model:main",
            "dump-model-version = mlflow_tools.display.dump_model_version:main",
            "dump-mlflow-model = mlflow_tools.display.dump_mlflow_model:main",
            "compare-model-versions = mlflow_tools.check_version.compare_model_versions:main",
            "check-model-version = mlflow_tools.check_version.check_model_version:main",
            "delete-model = mlflow_tools.tools.delete_model:main",
            "delete-model-versions = mlflow_tools.tools.delete_model_versions:main",
            "delete-model-stages = mlflow_tools.tools.delete_model_stages:main",
            "register-model = mlflow_tools.tools.register_model:main",
            "rename-model = mlflow_tools.tools.rename_model:main",
            "download-model = mlflow_tools.tools.download_model:main",
            "delete-experiment = mlflow_tools.tools.delete_experiment:main",
            "report-model-version = mlflow_tools.reports.report_model_version:main"
        ]
    }
)
