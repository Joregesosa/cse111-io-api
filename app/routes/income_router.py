from fastapi import APIRouter, Depends
from ..controllers.income_controller import index, show, store, update
from ..utils.get_token import get_token


income_router = APIRouter(prefix="/income", dependencies=[Depends(get_token)])

income_router.get("/")(index)

income_router.get("/{income_id}")(show)

income_router.post("/")(store)

income_router.put("/{income_id}")(update)
