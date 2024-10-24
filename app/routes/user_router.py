from typing import Union
from fastapi import APIRouter
from controllers.user_controller import index, show, store, update, destroy

user_router = APIRouter()

user_router.get("/users")(index)

user_router.get("/users/{user_id}")(show)

user_router.post("/users")(store)

user_router.put("/users/{user_id}")(update)

user_router.delete("/users/{user_id}")(destroy)


