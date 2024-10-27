from fastapi import HTTPException
from fastapi.responses import JSONResponse
from ..models.category_model import Category
from ..schemas.category_schema import CategorySchema
from fastapi import Request

async def index(request: Request):
    try:
        auth_user = request.state.auth_user
        category = Category()
        categories = await category.where("user_id", auth_user["id"])
        return categories
    except Exception as e:
        return e

async def show(request: Request, category_id: int):
    try:
        user_id = request.state.auth_user["id"]
        category = Category()
        _category = await category.find(category_id)
        if not _category or _category["user_id"] != user_id:
            return HTTPException(status_code=404, detail="Category not found")

        return _category
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

async def store(request: Request ,category: CategorySchema):
    try:
        print(category)
        auth_user = request.state.auth_user
        _category = Category()
        data = category.model_dump()
        data["user_id"] = auth_user["id"]
        await _category.create(data)
        return JSONResponse(status_code=201, content={"message": "category created successfully"})
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

async def update(request: Request ,category_id: int, category: CategorySchema):
    try:
        _category = Category()

        data = category.model_dump(exclude_unset=True)
        if not data:
            return HTTPException(status_code=400, detail="No data to update")

        exist = await _category.find(category_id)
        if not exist or exist["user_id"] != request.state.auth_user["id"]:
            return HTTPException(status_code=404, detail="Category not found")

        await _category.update(category_id, data)
        return {"message": "category updated successfully"}

    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

async def destroy(user_id: int):
    return {"message": f"Delete user {user_id}"}
