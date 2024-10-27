from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserSchema(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserSchemaUpdate(BaseModel):
    name: Optional[str] = Field(None, json_schema_extra={"example": "John Doe"})
    email: Optional[EmailStr] = Field(None, json_schema_extra={"example": "example@mail.com"})
    password: Optional[str] = Field(None, json_schema_extra={"example": "password123"})
