import hashlib

def calculate_file_hash(file_bytes: bytes) -> str:
    """
    Calculates the SHA-256 hash of a given byte sequence.
    This utility is MANDATORY for all evidence uploads to comply with
    Bhartiya Sakshya Adhiniyam (BSA) Section 63(4).
    
    Args:
        file_bytes (bytes): The raw bytes of the uploaded file.
        
    Returns:
        str: The hexadecimal representation of the SHA-256 hash.
    """
    sha256_hash = hashlib.sha256()
    sha256_hash.update(file_bytes)
    return sha256_hash.hexdigest()
