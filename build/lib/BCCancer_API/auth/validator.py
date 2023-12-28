import jwt
from jwt import PyJWTError
from fastapi import Depends, HTTPException, status, APIRouter, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from BCCancerAPI.dbmodels.conn_manager import get_rw_eng
from BCCancerAPI.dbmodels.emarc import User
from BCCancerAPI.dbmodels.mappers import user_to_dict
from os import getenv
from BCCancerAPI.dbmodels.config import Environ
from BCCancerAPI.utils.authutils import decode_token
env = Environ()

rw_eng = get_rw_eng()
rw_session = Session(rw_eng)
authapp = APIRouter()
# Configuration

SECRET_KEY = getenv("SECRET_KEY", env.env_config["SECRET_KEY"])
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        is_token_valid: bool = False
        payload = decode_token(jwtoken)

        if payload:
            is_token_valid = True
        return is_token_valid

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Mock user data for demonstration
fake_users_db = {
    "johndoe": {
        "useremail": "johndoe",
        "password": '$2b$12$O.V6/r3OG53mZl23qHByduJNq3dpbFbmHlZgKcXOZtxMIBM82LFZG',  # Hashed version of 'password123'
        "profile": "Admin",
        "token_exp": 600,
    },
    "sunny.rathee@phsa.ca":{
        "useremail": "sunny.rathee@phsa.ca",
        "password": '$2b$12$O.V6/r3OG53mZl23qHByduJNq3dpbFbmHlZgKcXOZtxMIBM82LFZG',  # Hashed version of 'password123'
        "profile": "EndUser",
        "token_exp": 60,
    }
}

# JWT token utilities
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    #print("Secret key=", SECRET_KEY)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username: str):
    results = rw_session.query(User).filter(User.useremail == username).all()
    if len(results) != 0:
        print(f"returning {results[0]}")
        return user_to_dict(results[0])


def authenticate_user(username: str, password: str):
    user = get_user(username)
    print(user)
    if not user:
        return False
    if not verify_password(password, user["password"]):
        return False
    return user



# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# Token endpoint
@authapp.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=user['token_exp'])
    access_token = create_access_token(
        data={"sub": user["useremail"], "profile": user['profile']}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Protected route

@authapp.get("/protected", dependencies=[Depends(JWTBearer())])
async def protected_route(request: Request, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print (payload)

        if payload.get("profile")!="Admin":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User doesnt have priviledges to access this endpoint",
                headers={"WWW-Authenticate": "Bearer"},
            )
        username = payload.get("sub")
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"message": "You have accessed a protected route"}




"""
# Main entry point
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""