import os
import shutil

def mk_dbfs_path(path):
    return path.replace("/dbfs","dbfs:")

def mk_local_path(path):
    return path.replace("dbfs:","/dbfs")

class DatabricksFileSystem(object):
    def __init__(self):
        import IPython
        self.dbutils = IPython.get_ipython().user_ns["dbutils"]

    def ls(self, path):
        return self.dbutils.fs.ls(path)

    def cp(self, src, dst, recursive=False):
        self.dbutils.fs.cp(mk_dbfs_path(src), mk_dbfs_path(dst), recursive)

    def rm(self, src, dst, recurse=False):
        self.dbutils.fs.rm(mk_dbfs_path(path), recurse)

    def mkdirs(self, path):
        self.dbutils.fs.mkdirs(path)

    def write(self, path, content):
        self.dbutils.fs.put(path, content, True)
            

class LocalFileSystem(object):
    def __init__(self):
        pass

    def cp(self, src, dst, recurse=False):
        shutil.copytree(mk_local_path(src), mk_local_path(dst))

    def rm(self, path, recurse=False):
        shutil.rmtree(mk_local_path(path))

    def mkdirs(self, path):
        os.makedirs(mk_local_path(path),exist_ok=True)

    def write(self, path, content):
        with open(mk_local_path(path), 'w') as f:
            f.write(content)

def get_filesystem():
    use_databricks = "DATABRICKS_RUNTIME_VERSION" in os.environ
    return DatabricksFileSystem() if use_databricks else LocalFileSystem()
