
def string_to_list(list_as_string):
    lst = list_as_string.split(",")
    if "" in lst: lst.remove("")
    return lst

def normalize_stages(stages):
    from mlflow.entities.model_registry import model_version_stages
    if stages is None:
        return []
    if isinstance(stages,str):
        stages = string_to_list(stages)
    stages = [ stage.lower() for stage in stages ]
    for stage in stages:
        if stage not in model_version_stages._CANONICAL_MAPPING:
            print(f"WARNING: stage '{stage}' must be one of: {model_version_stages.ALL_STAGES}")
    return stages
