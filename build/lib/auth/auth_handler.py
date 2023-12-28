# This file is responsible for signing , encoding , decoding and returning JWTS
import time
from typing import Dict

#from jwt import JWT
import jwt
JWT_SECRET = "8366760abcb91a43d60d07f18146850ec3abb4493f0a0674fea67cd56f5591fd"
JWT_ALGORITHM = "HS256"

#jwt=JWT()

def token_response(token: str):
    return {
        "access_token": token
    }

# function used for signing the JWT string

def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except Exception as e:
        return {}