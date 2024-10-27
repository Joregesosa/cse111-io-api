from ..config.app_config import app_config
from pydantic import BaseModel, EmailStr
from fastapi import HTTPException
from ..models.user_model import User
import bcrypt
import jwt


class AuthSchema(BaseModel):
    email: EmailStr
    password: str


async def login(auth: AuthSchema):
    try:
        user = User()
        _user = await user.where("email", auth.email)
        _user = _user[0] if _user else None
        if not _user:
            raise Exception("email or password is incorrect")
        
        if not bcrypt.checkpw(auth.password.encode(), _user["password"].encode()):
            raise Exception("email or password is incorrect")
        
        payload = {"id": _user["id"], "email": _user["email"]}
        token = jwt.encode(payload, app_config["APP_KEY"], algorithm="HS256")
        return {
            "token": token,
            "user": {"id": _user["id"], "email": _user["email"], "name": _user["name"]},
        }
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))
