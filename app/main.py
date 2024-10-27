from fastapi import FastAPI
from .routes.category_router import category_router
from .routes.auth_router import auth_router
from .middlewares.auth_middleware import auth_middleware
 
app = FastAPI()

app.middleware("http")(auth_middleware)

app.include_router(category_router, tags=["Category"])
app.include_router(auth_router, tags=["Auth"])
