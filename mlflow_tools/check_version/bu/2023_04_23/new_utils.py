
import mlflow

# == Download artifact issue

def download_artifacts(client, download_uri, dst_path=None, fix=True):
    """
    Apparently the tracking_uri argument is not honored for mlflow.artifacts.download_artifacts().
    It seems that tracking_uri is ignored and the global mlflow.get_tracking_uri() is always used.
    If the two happen to be the same operation will succeed.
    If not, it fails.
    Issue: Merge pull request #104 from mingyu89/fix-download-artifacts
    """
    if fix:
        previous_tracking_uri = mlflow.get_tracking_uri()
        mlflow.set_tracking_uri(client._tracking_client.tracking_uri)
        local_path = mlflow.artifacts.download_artifacts(
            artifact_uri = download_uri,
            dst_path = dst_path,
        )
        mlflow.set_tracking_uri(previous_tracking_uri)
    else:
        local_path = mlflow.artifacts.download_artifacts(
            artifact_uri = download_uri,
            dst_path = dst_path,
            tracking_uri = client._tracking_client.tracking_uri
        )
    return local_path
