import jwt
from os import getenv
from BCCancerAPI.dbmodels.config import Environ
import time
from fastapi import Request
from fastapi.security.utils import get_authorization_scheme_param
from fastapi import HTTPException, status
env = Environ()

SECRET_KEY = getenv("SECRET_KEY", env.env_config["SECRET_KEY"])
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def decode_token(token):
    try:
        print("DECODING WITH :"+SECRET_KEY)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        payload = payload if payload.get("exp") >= time.time() else None
    except Exception as e:
        print(e)
        raise HTTPException(403, "Invalid token.")
    return payload


async def get_authorization_payload(request: Request):
    authorization = request.headers.get("Authorization")
    scheme, credentials = get_authorization_scheme_param(authorization)
    if scheme == 'Bearer':
        payload = decode_token(credentials)
        return payload
    return None

def has_role(required_role: str, request:Request):

    payload = get_authorization_payload(request)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Wrong scheme",
        )
    print(payload)
    role=payload.get("profile")
    print(f"profile:{role}")
    if role != required_role:
        print("raising error")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this resource",
        )
