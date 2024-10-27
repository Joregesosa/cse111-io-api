from typing import Annotated
from fastapi import Depends
from fastapi.security import APIKeyHeader

oauth2_scheme =  APIKeyHeader(name="Authorization")

def get_token(token: Annotated[str, Depends(oauth2_scheme)]):
    return token
