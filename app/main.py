from typing import Union
from fastapi import FastAPI
from routes.user_router import user_router
from routes.category_router import category_router

app = FastAPI(prefix="/api/v1")

app.include_router(user_router, tags=["User"])
app.include_router(category_router, tags=["Category"])

 