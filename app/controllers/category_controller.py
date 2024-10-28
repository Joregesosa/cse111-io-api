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
        return JSONResponse(status_code=200, content={"data": categories})
    except Exception as e:
        return JSONResponse(status_code=400, content={"details": str(e)})

async def show(request: Request, category_id: int):
    try:
        user_id = request.state.auth_user["id"]
        category = Category()
        _category = await category.find(category_id)
        if not _category or _category["user_id"] != user_id:
            return JSONResponse(status_code=404, content={"details": "category not found"})

        return _category
    except Exception as e:
        return JSONResponse(status_code=400, content={"details": str(e)})

async def store(request: Request ,category: CategorySchema):
    try:
        auth_user = request.state.auth_user
        exist = await Category().where("name", category.name)
        if exist and exist[0]["user_id"] == auth_user["id"]:
            return JSONResponse(status_code=400, content={"details": "category already exists"})
        
        _category = Category()
        data = category.model_dump()
        data["user_id"] = auth_user["id"]
        await _category.create(data)
        return JSONResponse(status_code=201, content={"details": "category created successfully"})
    except Exception as e:
        return JSONResponse(status_code=400, content={"details": str(e)})

async def update(request: Request ,category_id: int, category: CategorySchema):
    try:
        _category = Category()

        data = category.model_dump(exclude_unset=True)
        if not data:
            return JSONResponse(status_code=400, content={"details": "No data to update"})

        exist = await _category.find(category_id)
        if not exist or exist["user_id"] != request.state.auth_user["id"]:
            return JSONResponse(status_code=404, content={"details": "Category not found"})

        await _category.update(category_id, data)
        return JSONResponse(status_code=200, content={"details": "category updated successfully"})

    except Exception as e:
        return JSONResponse(status_code=400, content={"details": str(e)})

async def destroy(user_id: int):
    return {"message": f"Delete user {user_id}"}
