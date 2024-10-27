from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class RegisterSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    
class PasswordSchema(BaseModel):
    oldpassword: str = Field(..., json_schema_extra={"example": "oldpassword"})
    newpassword: str = Field(..., json_schema_extra={"example": "newpassword"}) 

class UpdateSchema(BaseModel):
   name: Optional[str] = Field(None, json_schema_extra={"example": "John Doe"})
   email: Optional[EmailStr] = Field(None, json_schema_extra={"example": "example@mail.com"})
     