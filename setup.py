from setuptools import setup

setup(name="mlflow_tools",
      version="1.0.0",
      author="Andre M",
      description="MLflow Tools",
      url="https://github.com/amesar/mlflow-tools",
      packages=['mlflow_tools',
                'mlflow_tools.common',
                'mlflow_tools.tools',
                'mlflow_tools.export_import'
                ],
      zip_safe=False)
