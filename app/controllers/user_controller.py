from fastapi import HTTPException
from ..models.user_model import User
from ..schemas.user_schema import UserSchema, UserSchemaUpdate
import bcrypt


async def index():
    try:
        user = User()
        users = await user.all()
        return users
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))


async def show(user_id: int):
    try:
        user = User()
        user = await user.find(user_id)
        if not user:
            return HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))


async def store(user: UserSchema):
    try:
        _user = User()
        data = user.model_dump()
        hash = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt())
        data["password"] = hash.decode()
        new_user = await _user.create(data)
        return {"message": "User created", "user_id": new_user}
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))


async def update(user_id: int, user: UserSchemaUpdate):
    try:
        _user = User()
        
        data = user.model_dump(exclude_unset=True)
        
        exist = await _user.find(user_id)
        if not exist:
            return HTTPException(status_code=404, detail="User not found")
        
        if not data:
            return HTTPException(status_code=400, detail="No data to update")

        if "password" in data:
            hash = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt())
            data["password"] = hash.decode()

        await _user.update(user_id, data)
        return {"message": "User updated successfully"}
    except Exception as e:
         return HTTPException(status_code=400, detail=str(e))

async def destroy(user_id: int):
    return {"message": f"Delete user {user_id}"}
