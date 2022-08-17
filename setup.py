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
    python_requires = ">=3.7",
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        "mlflow>=1.26.0",
        "pytest==5.3.5",
        "wheel"
    ],
    license = "Apache License 2.0",
    keywords = "mlflow ml ai",
    classifiers = [
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent"
    ],
)
