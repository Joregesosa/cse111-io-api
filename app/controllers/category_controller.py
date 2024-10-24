import http
from fastapi import HTTPException
from models.category_model import Category
from schemas.category_schema import CategorySchema


def index():
    try:
        category = Category()
        categories = category.all()
        return categories
    except Exception as e:
        return e


def show(category_id: int):
    try:
        category = Category()
        _category = category.find(category_id)
        print(_category)
        if not _category:
            return HTTPException(status_code=404, detail="Category not found")

        return _category
    except Exception as e:
        return e


def store(category: CategorySchema):
    try:
        _category = Category()
        data = category.model_dump()
        print()
        new_category = _category.create(data)
        return {"message": "category created successfully", "user_id": new_category}
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))


def update(category_id: int, category: CategorySchema):
    try:
        _category = Category()

        data = category.model_dump(exclude_unset=True)
        if not data:
            return HTTPException(status_code=400, detail="No data to update")
        
        exist = _category.find(category_id)
        if not exist:
            return HTTPException(status_code=404, detail="Category not found")

        _category.update(category_id, data)
        return {"message": "category updated sucessfully"}
    
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))


def destroy(user_id: int):
    return {"message": f"Delete user {user_id}"}
