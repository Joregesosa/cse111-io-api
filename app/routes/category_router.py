 
from fastapi import APIRouter, Depends
from ..controllers.category_controller import index, show, store, update
from ..utils.get_token import get_token


category_router = APIRouter(prefix="/category", dependencies=[Depends(get_token)])


category_router.get("/")(index)

category_router.get("/{user_id}")(show)

category_router.post("/")(store)

category_router.put("/{user_id}")(update) 

# category_router.delete("/{user_id}")(destroy)
