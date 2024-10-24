from typing import Union
from fastapi import APIRouter
from controllers.category_controller import index, show, store, update, destroy

category_router = APIRouter(prefix="/category")

category_router.get("/")(index)

category_router.get("/{user_id}")(show)

category_router.post("/")(store)

category_router.put("/{user_id}")(update)

category_router.delete("/{user_id}")(destroy)


