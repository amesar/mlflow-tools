
import mlflow
import filecmp

def compare_dirs(dir1, dir2):
    #print(">> ======= diff")
    dcmp = filecmp.dircmp(dir1, dir2)
    #print(">> dir1:",dir1)
    #print(">> dir2:",dir2)
    dcmp = filecmp.dircmp(dir1, dir2)
    equals = dcmp.left_only==[] and dcmp.right_only==[] and dcmp.diff_files==[]
    #print(f"EQ: {equals}")
    dct = {
        "equals": equals,
        "dir1": dir1,
        "dir2": dir2,
    }

    if True:
    #if not res:
        diff = {
            "diff_files": dcmp.diff_files,
            "left_only": dcmp.left_only,
            "right_only": dcmp.right_only,
            "same_files": dcmp.same_files
        }
        dct["differences"] = diff
    #print(">> compare:",dct)
    return dct

def compare_files(file1, file2):
    with open(file1, "rb") as f1, open(file2, "rb") as f2:
        return f1.read() == f2.read()


def dump(x, msg=""):
    if isinstance(x,dict):
        dump_dct(x, msg)
    else:
        dump_obj(x, msg)

def dump_dct(dct, msg=""):
    import json
    print(f"{msg}:")
    print(json.dumps(dct, indent=2)+"\n")

def dump_obj(obj, msg=""):
    print("------")
    print(f"Dump {msg}:")
    for k,v in obj.__dict__.items():
        print(f"  {k}: {v}")
    print("------")
