import jwt
from ..config.app_config import app_config
from fastapi.responses import JSONResponse

guest_routes = [
    "/auth/login",
    "/auth/register",
    "/openapi.json",
    "/favicon.ico",
    "/docs",
]

async def auth_middleware(request, call_next):
    try:
        if request.url.path not in guest_routes:
            
            if not request.headers.get("Authorization"):
                return JSONResponse({"error": "missing Authorization header"}, status_code=401)
            
            token = request.headers.get("Authorization") 
            if not token:
                return JSONResponse({"error": "no token provided"}, status_code=401)
        
            payload = jwt.decode(token, app_config["APP_KEY"], algorithms=["HS256"])
            
            if not payload:
                return JSONResponse({"error": "invalid token"}, status_code=401)
            
            request['state']['auth_user'] = payload
            
        response = await call_next(request)
        return response
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
