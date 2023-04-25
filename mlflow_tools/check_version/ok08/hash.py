

path = "hash.py"

def test_hashlib(path):
    import hashlib
    hash = hashlib.md5(open(path,'rb').read()).hexdigest()
    print("hashlib: hash:",hash)

def test_checksumdir(path):
    from checksumdir import dirhash
    print("checksumdir:")

    md5hash    = dirhash(path, "md5")
    print("  md5hash:   ",md5hash)

    #sha1hash    = dirhash(path, "sha1hash") # NotImplementedError: sha1hash not implemented.
    #print("  sha1hash:  ",sha1hash) 

    #sha256hash    = dirhash(path, "sha256hash") # NotImplementedError: sha256hash not implemented.
    #print("  sha256hash:",sha256hash)

def main(path):
    print("path:",path)
    test_hashlib(path)
    test_checksumdir("bu")

if __name__ == "__main__":
    main(path)
