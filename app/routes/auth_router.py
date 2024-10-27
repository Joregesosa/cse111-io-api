from fastapi import APIRouter
from ..controllers.auth_controller import login, register, me, update_user, change_password

auth_router = APIRouter(prefix="/auth")

auth_router.post("/login")(login)

auth_router.post("/register")(register)

auth_router.get("/me")(me)

auth_router.post("/update")(update_user)

auth_router.post("/change-password")(change_password)