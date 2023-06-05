import json

def obj_to_dict(obj):
    """ Recursively convert and object to a dict. """
    return json.loads(
        json.dumps(obj, default=lambda o: getattr(o, '__dict__', str(o)))
    )   


def dump_dict_as_json(dct):
    print(json.dumps(dct, indent=2))


def scrub_dict(obj, bad_key):
    """
    Recursively delete a key from a nested dict.
    From: https://stackoverflow.com/questions/20692710/python-recursively-deleting-dict-keys
    """
    if isinstance(obj, dict):
        for key in list(obj.keys()): 
            if key == bad_key:
                del obj[key]
            else:
                scrub_dict(obj[key], bad_key)
    elif isinstance(obj, list):
        for i in reversed(range(len(obj))):
            if obj[i] == bad_key:
                del obj[i]
            else:
                scrub_dict(obj[i], bad_key)
    else:
        # neither a dict nor a list, do nothing
        pass 
