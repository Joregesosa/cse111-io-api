from typing import Union
from fastapi import APIRouter, Depends
from ..controllers.user_controller import index, show, store, update, destroy
from ..utils.get_token import get_token


user_router = APIRouter(prefix="/users", dependencies=[Depends(get_token)])

user_router.get("/")(index)

user_router.get("/{user_id}")(show)

user_router.post("/")(store)

user_router.put("/{user_id}")(update)

user_router.delete("/{user_id}")(destroy)


