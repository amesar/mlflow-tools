from setuptools import setup, find_packages

setup(name="mlflow_tools",
      version="1.0.0",
      author="Andre M",
      description="MLflow Tools",
      url="https://github.com/amesar/mlflow-tools",
      packages=find_packages(),
      zip_safe=False,
      install_requires=[
          "mlflow>=1.19.0",
          "pytest==5.3.5",
          "wheel"
      ])
