from fastapi import APIRouter, Depends
from ..controllers.expense_controller import index, show, store, update
from ..utils.get_token import get_token


expense_router = APIRouter(prefix="/expense", dependencies=[Depends(get_token)])

expense_router.get("/")(index)

expense_router.get("/{expense_id}")(show)

expense_router.post("/")(store)

expense_router.put("/{expense_id}")(update)

# expense_router.delete("/{expense_id}")(destroy)