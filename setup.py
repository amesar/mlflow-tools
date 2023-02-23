from setuptools import setup, find_packages

setup(
    name="mlflow_tools",
    version="1.0.0",
    author="Andre Mesarovic",
    description="MLflow Tools",
    long_description=open("README.md").read(),
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
        "mlflow>=1.30.0",
        "wheel"
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
            "dump-run = mlflow_tools.tools.dump_run:main",
            "dump-experiment = mlflow_tools.tools.dump_experiment:main",
            "dump-model = mlflow_tools.tools.dump_model:main",
            "list-experiments = mlflow_tools.tools.list_experiments:main",
            "list-models = mlflow_tools.tools.list_models:main",
            "list-model-versions = mlflow_tools.tools.list_model_versions:main"
        ]
    }
)
