from ..config.app_config import app_config
from ..schemas.auth_schema import LoginSchema, RegisterSchema, PasswordSchema,UpdateSchema
from ..utils.get_token import get_token
from ..models.user_model import User
from fastapi import Depends, Request
from fastapi.responses import JSONResponse
import bcrypt
import jwt




async def login(auth: LoginSchema) -> JSONResponse:
    try:
        user = User()
        _user = await user.where("email", auth.email)
        
        _user = _user[0] if _user else None
        
        print(_user)
        
        
        if not _user:
            return JSONResponse(status_code=400, content={"details": "email or password is incorrect"})
        
        if not bcrypt.checkpw(auth.password.encode(), _user["password"].encode()):
           return JSONResponse(status_code=400, content={"details": "email or password is incorrect"})
        
        payload = {"id": _user["id"], "email": _user["email"]}
        token = jwt.encode(payload, app_config["APP_KEY"], algorithm="HS256")
        #eliminar password del diccionario user
        del _user["password"]
        return JSONResponse(status_code=200, content={"token": token, "user": _user})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=400, content={"details": str(e)})

async def register(auth: RegisterSchema) -> JSONResponse:
    try:
        user = User()
        _user = await user.where("email", auth.email)
        if _user:
            return JSONResponse(status_code=400, content={"details": "user already exists"})
        
        hashed_password = bcrypt.hashpw(auth.password.encode(), bcrypt.gensalt())
        new_user = auth.model_dump()
        new_user["password"] = hashed_password.decode()
        await user.create(new_user)

        return JSONResponse(status_code=201, content={"details": "user created successfully"})
    except Exception as e:
        return JSONResponse(status_code=400, content={"details": str(e)})  

async def me(request: Request, token: str = Depends(get_token)) -> JSONResponse:
    try:
        user_id = request.state.auth_user["id"]
        user =  User()
        _user = await user.find(user_id)
        
        if not _user:
            return JSONResponse(status_code=404, content={"details": "User not found"})
        
        return JSONResponse(status_code=200, content={"user": _user})
    
    except Exception as e:
        return JSONResponse(status_code=400, content={"details": str(e)})

async def change_password(request: Request, body: PasswordSchema , token: str = Depends(get_token)) -> JSONResponse:
    try:
        user_id = request.state.auth_user["id"]
        user = User()
        _user = await user.find(user_id)
        
        if not _user:
            return JSONResponse(status_code=404, content={"details": "User not found"})
        
        if not bcrypt.checkpw(body.oldpassword.encode(), _user["password"].encode()):
            return JSONResponse(status_code=400, content={"details": "old password is incorrect"})
        
        hashed_password = bcrypt.hashpw(body.newpassword.encode(), bcrypt.gensalt())
        await user.update(user_id, {"password": hashed_password.decode()})
        return JSONResponse(status_code=200, content={"details": "password updated successfully"})
    except Exception as e:
        return JSONResponse(status_code=400, content={"details": str(e)})
    
async def update_user(request: Request, user: UpdateSchema, token: str = Depends(get_token)) -> JSONResponse:
    try:
         print('here')
         user_id = request.state.auth_user["id"]
         body = user.model_dump(exclude_unset=True)
         if not body:
             return JSONResponse(status_code=400, content={"details": "No data to update"})
         _user = User()
         await _user.update(user_id, body)
         return JSONResponse(status_code=200, content={"details": "user updated successfully"})
    except Exception as e:
        return JSONResponse(status_code=400, content={"details": str(e)}) 