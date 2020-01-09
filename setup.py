from setuptools import setup

setup(name='mlflow_tools',
      version='0.0.1',
      description='MLflow Tools',
      author='Andre',
      packages=['mlflow_tools',
                'mlflow_tools.common',
                'mlflow_tools.tools',
                'mlflow_tools.export_import',
                'mlflow_tools.make_exps_page'
                ],
      zip_safe=False)
