from fastapi.responses import JSONResponse
from ..models.balance_model import Balance
from fastapi import Request


async def show(request: Request):
    try:
        auth_user = request.state.auth_user
        balance = Balance()
        _balance = await balance.where({"user_id": auth_user["id"]})
        _balance = _balance[0] if _balance else None
        print(_balance)
        return JSONResponse(status_code=200, content={"data": _balance})
    except Exception as e:
        return JSONResponse(status_code=400, content={"details": str(e)})
    


