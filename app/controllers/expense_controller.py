from typing import Optional
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from ..models.expense_model import Expense
from ..models.balance_model import Balance
from fastapi import Request

class ExpenseSchema(BaseModel):
    category_id: int
    amount: int
    description: str
    expense_date: Optional[str] = Field(None, json_schema_extra={"example": "2021-09-01"})


async def index(request: Request):
    try:
        print(request.state.auth_user)
        expense = Expense()
        user_id = request.state.auth_user["id"]
        expenses = await expense.where({"user_id": user_id})
        return JSONResponse(status_code=200, content={"data": expenses})
    except Exception as e:
        return JSONResponse(status_code=400, content={"details": str(e)})


async def show(request: Request, expense_id: int):
    try:
        user_id = request.state.auth_user["id"]
        expense = Expense()
        _expense = await expense.find(expense_id)
        if not _expense or _expense["user_id"] != user_id:
            return JSONResponse(
                status_code=404, content={"details": "expense not found"}
            )
        return JSONResponse(status_code=200, content={"data": _expense})

    except Exception as e:
        return JSONResponse(status_code=400, content={"details": str(e)})


async def store(request: Request, expense: ExpenseSchema):
    try:
        balance = Balance()
        _expense = Expense()

        data = expense.model_dump(exclude_unset=True)

        user_id = request.state.auth_user["id"]
        current_balance = await balance.where({"user_id": user_id})

        r_balance = current_balance[0]["amount"] - data["amount"]

        data["r_balance"] = r_balance

        data["user_id"] = user_id

        await _expense.create(data)

        return JSONResponse(
            status_code=201, content={"details": "expense created successfully"}
        )
    except Exception as e:
        return JSONResponse(status_code=400, content={"details": str(e)})
    

async def update(request: Request, expense_id: int, expense: ExpenseSchema):
    try:
        user_id = request.state.auth_user["id"]
        _expense = Expense()
        balance = Balance()

        current_balance = await balance.where({"user_id": user_id})
        data = expense.model_dump(exclude_unset=True)
        if not data:
            return JSONResponse(status_code=400, content={"details": "No data to update"})

        exist = await _expense.find(expense_id)
        if not exist or exist["user_id"] != request.state.auth_user["id"]:
            return JSONResponse(status_code=404, content={"details": "Expense not found"})
        
        r_balance = current_balance[0]["amount"] + exist["amount"] - data["amount"]
        data["r_balance"] = r_balance

        await _expense.update(expense_id, data)
        return JSONResponse(
            status_code=200, content={"details": "expense updated successfully"}
        )
    except Exception as e:
        return JSONResponse(status_code=400, content={"details": str(e)})