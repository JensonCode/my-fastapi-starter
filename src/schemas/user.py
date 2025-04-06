from pydantic import BaseModel
from pydantic.config import ConfigDict
from datetime import datetime


class UserBase(BaseModel):
    id: int
    username: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RegisterFormData(BaseModel):
    username: str
    password: str


class RegisterResponse(BaseModel):
    access_token: str
    token_type: str


class LoginFormData(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
