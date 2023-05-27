"""
Display utilities
"""

from mlflow_tools.client.http_client import MlflowHttpClient

http_client = MlflowHttpClient()


def process_df(df, columns=None, sort_attr="name", sort_order="asc", csv_file=None):
    if columns:
        df = df[columns]
    if sort_attr in df.columns:
        df.sort_values(by=[sort_attr], inplace=True, ascending=sort_order == "asc")
    if csv_file:
        with open(csv_file, "w", encoding="utf-8") as f:
            df.to_csv(f, index=False)
    return df

from dataclasses import dataclass

def build_artifacts(run_id, path, artifact_max_level, level=0):
    """
    Build recursive tree of calls to 'artifacts/list' API endpoint.
    :param run_id: Run ID.
    :param path: Relative artifact path.
    :param artifact_max_level: Levels to recurse.
    :return: List of Result object representing tree node info
    """
    @dataclass()
    class Result:
        artifacts: dict = None
        num_bytes: int = 0
        num_artifacts: int = 0
        num_levels: int = 0
        def __repr__(self):
            return f"{self.num_bytes} {self.num_artifacts} {self.num_levels} {self.artifacts}"

    if level == artifact_max_level:
        return Result({}, 0, 0, level)
    artifacts = http_client.get(f"artifacts/list", { "run_id": run_id, "path": path })
    if level > artifact_max_level:
        return Result(artifacts, 0, 0, level)
    num_bytes, num_artifacts = (0,0)

    files = artifacts.get("files",None)
    if files:
        for _,artifact in enumerate(files):
            num_bytes += int(artifact.get("file_size",0)) or 0
            if artifact["is_dir"]:
                res = build_artifacts(run_id, artifact["path"], artifact_max_level, level+1)
                num_bytes += res.num_bytes
                num_artifacts += res.num_artifacts
                artifact["artifacts"] = res.artifacts
            else:
                num_artifacts += 1

    return Result(artifacts, num_bytes, num_artifacts, level)
