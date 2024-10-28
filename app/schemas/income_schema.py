from pydantic import BaseModel

class IncomeSchema(BaseModel):
    amount: float
    description: str