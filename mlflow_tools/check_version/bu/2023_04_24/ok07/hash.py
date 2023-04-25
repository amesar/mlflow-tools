

import hashlib

path = "tt20"
x = hashlib.md5(open(path,'rb').read()).hexdigest()
print("path:",path)
print("hash:",x)
print("hash:",type(x))
