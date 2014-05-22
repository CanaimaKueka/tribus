

def compute_file_hash(hash_type, filename):
    """Simple helper to compute the digest of a file.

    @param hash_type: A class like hashlib.sha256.
    @param filename: File path to compute the digest from.
    """
    hash = hash_type()
    with open(filename) as file:
        # Chunk the digest extraction to avoid loading large
        # files in memory unnecessarily. 
        while True:
            chunk = file.read(8192)
            if not chunk:
                break
            hash.update(chunk)
    return hash.hexdigest()
