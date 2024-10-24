from fastapi import HTTPException
from models.user_model import User
from schemas.user_schema import UserSchema, UserSchemaUpdate
import bcrypt


def index():
    try:
        user = User()
        users = user.all()
        return users
    except Exception as e:
        return e


def show(user_id: int):
    try:
        user = User()
        user = user.find(user_id)
        return user
    except Exception as e:
        return e


def store(user: UserSchema):
    try:
        _user = User()
        data = user.model_dump()
        hash = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt())
        data["password"] = hash.decode()
        new_user = _user.create(data)
        return {"message": "User created", "user_id": new_user}
    except Exception as e:
        return e


def update(user_id: int, user: UserSchemaUpdate):
    try:
        _user = User()
        
        data = user.model_dump(exclude_unset=True)
         
        if not data:
            return HTTPException(status_code=400, detail="No data to update")

        if "password" in data:
            hash = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt())
            data["password"] = hash.decode()

        _user.update(user_id, data)
        return {"message": "User updated sucessfully"}
    except Exception as e:
         return HTTPException(status_code=400, detail=str(e))


def destroy(user_id: int):
    return {"message": f"Delete user {user_id}"}
