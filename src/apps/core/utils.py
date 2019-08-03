import hashlib
import random
from datetime import datetime


def create_hash(d=None):
    """
    returns a hashed string of 64 chars with a dict param.
    """
    small_entropy = random.randint(0, 100000)
    hash_object = ""
    if d is not None:
        for row in d:
            hash_object += str(hashlib.sha256(row.encode('utf-8')).hexdigest())
    hash_object += str(hashlib.sha256(datetime.now().strftime(
        "%H:%M:%S.%f").encode('utf-8')).hexdigest())
    hash_object += str(small_entropy)
    return str(hashlib.sha256(hash_object.encode('utf-8')).hexdigest())[-64:]
