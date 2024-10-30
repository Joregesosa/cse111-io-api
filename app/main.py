from fastapi import FastAPI
from .routes.category_router import category_router
from .routes.auth_router import auth_router
from .routes.income_router import income_router
from .routes.expense_router import expense_router
from .routes.balance_router import balance_router
from .middlewares.auth_middleware import auth_middleware
 
app = FastAPI()

app.middleware("http")(auth_middleware)

app.include_router(category_router, tags=["Category"])
app.include_router(auth_router, tags=["Auth"])
app.include_router(income_router, tags=["Income"])
app.include_router(expense_router, tags=["Expense"])
app.include_router(balance_router, tags=["Balance"])