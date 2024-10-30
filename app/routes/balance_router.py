from fastapi import APIRouter, Depends
from ..controllers.balance_controller import show
from ..utils.get_token import get_token

balance_router = APIRouter(prefix="/balance", dependencies=[Depends(get_token)])

balance_router.get("/")(show)

