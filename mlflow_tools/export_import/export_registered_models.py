""" 
Exports registered models.
"""

import os
import click
from mlflow_tools.common.http_client import HttpClient

api_prefix = "api/2.0/preview/mlflow"
resource = "registered-models/list"

class RegisteredModelsExporter():
    def __init__(self, client=None, output="."):
        self.client = client if client else HttpClient(api_prefix)
        self.output = output
        print("HTTP client:",self.client)

    def export_registered_models(self):
        rsp = self.client._get(resource)
        path = os.path.join(self.output,"registered_models.json")
        print("Output file:",path)
        with open(path, 'w') as f:
            f.write(rsp.text)

@click.command()
@click.option("--output", help="Output path", default=".", type=str)
def main(output):
    print("Options:")
    for k,v in locals().items():
        print(f"  {k}: {v}")
    exporter = RegisteredModelsExporter(None, output)
    exporter.export_registered_models()

if __name__ == "__main__":
    main()
