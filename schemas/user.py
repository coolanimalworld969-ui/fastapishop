from typing import Literal

from pydantic import BaseModel, ValidationError, EmailStr, Field, ConfigDict
import email_validator


class UserResponse(BaseModel):
    username: str
    age: int = Field(gt=0,le=100)
    email: EmailStr
    id: int

    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    username: str
    age: int = Field(gt=0, le=100)
    email: EmailStr
    password: str

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    age: int | None = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"]

class UserChangePass(BaseModel):
    old_password: str
    new_password: str