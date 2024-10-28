from fastapi.responses import JSONResponse
from ..schemas.income_schema import IncomeSchema
from ..models.income_model import Income
from ..models.balance_model import Balance
from fastapi import Request

async def index(request: Request):
    try:
        auth_user = request.state.auth_user
        income = Income()
        incomes = await income.where({"user_id": auth_user["id"]})
        return JSONResponse(status_code=200, content={"data": incomes})
    except Exception as e:
        return JSONResponse(status_code=400, content={"details": str(e)})

async def show(request: Request, income_id: int):
    try:
        user_id = request.state.auth_user["id"]
        income = Income()
        _income = await income.find(income_id)
        if not _income or _income["user_id"] != user_id:
            return JSONResponse(status_code=404, content={"details": "income not found"})

        return _income
    except Exception as e:
        return JSONResponse(status_code=400, content={"details": str(e)})

async def store(request: Request ,income: IncomeSchema):
    try:
        balance = Balance()
        _income = Income()
        data = income.model_dump(exclude_unset=True)
        user_id = request.state.auth_user["id"]
        current_balance = await balance.where({"user_id": user_id})

        r_balance = current_balance[0]["amount"] + data['amount']
        
        data['r_balance'] = r_balance 
        data["user_id"] = user_id

        print(data)

        await _income.create(data)

        return JSONResponse(status_code=201, content={"details": "income created successfully"})
    except Exception as e:
        return JSONResponse(status_code=400, content={"details": str(e)})

async def update(request: Request ,income_id: int, income: IncomeSchema):
    try:
        user_id = request.state.auth_user["id"] 
        _income = Income()
        balance = Balance()
        
        current_balance = await balance.where({"user_id": user_id})
        data = income.model_dump(exclude_unset=True)
        if not data:
            return JSONResponse(status_code=400, content={"details": "No data to update"})

        exist = await _income.find(income_id)
        if not exist or exist["user_id"] != request.state.auth_user["id"]:
            return JSONResponse(status_code=404, content={"details": "Income not found"})

        pos_incomes = await _income.query(f"SELECT * FROM incomes WHERE user_id = {user_id}  AND created_at > '{exist['created_at']}'")
        if pos_incomes:
            return JSONResponse(status_code=400, content={"details": "Cannot update income after another transaction has been made"})
        
        
        
        # pos_expenses = await _income.query(f"SELECT * FROM expenses WHERE user_id = {user_id} AND created_at > {exist['created_at']}")

        # if pos_expenses:
        #     return JSONResponse(status_code=400, content={"details": "Cannot update income after another transaction has been made"})

        r_balance = current_balance[0]["amount"] - exist["amount"] + data["amount"]
        data["r_balance"] = r_balance

        await _income.update(income_id, data)
        return JSONResponse(status_code=200, content={"details": "income updated successfully"})
    except Exception as e:
        return JSONResponse(status_code=400, content={"details": str(e)})