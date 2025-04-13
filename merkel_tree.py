import hashlib
def calculate_merkle_root_whole_string(data, chunk_size):
    chunk_hashes = []
    if not data:
        return hashlib.sha256(b'').hexdigest()
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        chunk_hash = hashlib.sha256(chunk).hexdigest()
        chunk_hashes.append(chunk_hash)

    while len(chunk_hashes) > 1:
        new_hashes = []
        if len(chunk_hashes) % 2 != 0:
            chunk_hashes.append(chunk_hashes[-1])

        for i in range(0, len(chunk_hashes), 2):
            hash1 = chunk_hashes[i]
            hash2 = chunk_hashes[i + 1]
            combined = hash1.encode('utf-8') + hash2.encode('utf-8')
            new_hash = hashlib.sha256(combined).hexdigest()
            new_hashes.append(new_hash)

        chunk_hashes = new_hashes

    return chunk_hashes[0]