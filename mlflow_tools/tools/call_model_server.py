"""
Call MLflow model server with a split-oriented JSON file.
"""

import json
import click
import requests

@click.command()
@click.option("--api-uri", help="API URI.", required=True)
@click.option("--token", help="Databricks token (PAT).", default=None, type=str)
@click.option("--datapath", help="Data path.", required=True)

def main(api_uri, token, datapath):
    print("Options:")
    for k,v in locals().items(): print(f"  {k}: {v}")

    with open(datapath, "r") as f:
        data = json.loads(f.read())

    data = json.dumps(data)
    headers = { "Content-Type": "application/json" }
    if token:
        headers["Authorization"] = f"Bearer {token}" 
    rsp = requests.post(api_uri, headers=headers, data=data)
    if rsp.status_code < 200 or rsp.status_code > 299:
        raise Exception(f"HTTP status code: {rsp.status_code}. Reason: {rsp.reason} URL: {api_uri}")
    print("Predictions:\n", json.loads(rsp.text))

if __name__ == "__main__":
    main()
