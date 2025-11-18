from fastapi import APIRouter
import hashlib

router = APIRouter()

def normalized_query_hash(query:str)->str:
    """
    Returns a SHA-256 hash of a normalized query string.

    The normalization involves stripping leading/trailing whitespace and
    converting the string to lowercase.

    The resulting hash is a 64-character hexadecimal string.

    :param query: The query string to be normalized and hashed
    :type query: str
    :return: A SHA-256 hash of the normalized query string
    :rtype: str
    """
    normalized_query = query.strip().lower()
    encoded_query = normalized_query.encode('utf-8')
    hashed_query = hashlib.sha256(encoded_query)
    hex_query = hashed_query.hexdigest()
    return hex_query


@router.get('/hash')
async def hash_query(query:str):
    result = normalized_query_hash()
    return {'Plain Query ':query,'Hashed Query ':result}