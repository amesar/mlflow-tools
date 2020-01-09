""" 
Exports registered models.
"""

import os
from mlflow_tools.common.http_client import HttpClient

api_prefix = "api/2.0/preview/mlflow"
resource = "registered-models/list"

class RegisteredModelsExporter(object):
    def __init__(self, client=None, output="."):
        self.client = HttpClient(api_prefix)
        self.output = output
        print("HTTP client:",self.client)

    def export_registered_models(self):
        rsp = self.client._get(resource)
        path = os.path.join(self.output,"registered_models.json")
        print("Output file:",path)
        with open(path, 'w') as f:
            f.write(rsp.text)
        
if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--output", dest="output", help="Output", default=".", required=False)
    args = parser.parse_args()
    print("Options:")
    for arg in vars(args):
        print("  {}: {}".format(arg,getattr(args, arg)))
    exporter = RegisteredModelsExporter(None, args.output)
    exporter.export_registered_models()
