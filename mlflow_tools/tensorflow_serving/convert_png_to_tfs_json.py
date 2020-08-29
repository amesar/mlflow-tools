"""
Convert an MNIST PNG file to TensorFlow Serving JSON format.
"""
import sys
import json
import numpy as np
from PIL import Image

if __name__ == "__main__":
    data = np.asarray(Image.open(sys.argv[1]))
    data = data.reshape((1, 28 * 28))
    dct = { "instances" : [ data[0].tolist()] }
    print(json.dumps(dct,indent=2)+"\n") 
