from BCCancerAPI.dbmodels.emarc import User
#from main import rw_session
from BCCancerAPI.auth.validator import get_password_hash
from pydantic import EmailStr,BaseModel, Field,constr
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException
from BCCancerAPI.dbmodels.conn_manager import get_rw_eng
from enum import Enum

rw_eng = get_rw_eng()
rw_session = Session(rw_eng)

userapp = APIRouter()





class Profile(str,Enum):
    ENDUSER = "EndUser"
    ADMIN = "Admin"

class UserSchema(BaseModel):
    useremail: EmailStr
    profile: Profile
    password: constr(max_length=32)
    token_exp: int = Field(default=600)


@userapp.post("/user/create", tags=["User"])
async def create_user(user: UserSchema):
    try:
        """Create ability to send otp email/ verification email
        Create endpoint for Verification"""
        row = User(profile=Profile.ENDUSER.value,
                   useremail=user.useremail,
                   password=get_password_hash(user.password),
                   token_exp=user.token_exp)
        rw_session.add(row)
        rw_session.commit()
    except Exception as e:
        rw_session.rollback()
        raise HTTPException(400, e.__str__())
    return {"Success": True}

