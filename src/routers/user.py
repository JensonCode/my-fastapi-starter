from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from ..services.user import UserService
from ..deps.jwt import create_access_token
from ..schemas.user import LoginResponse, RegisterFormData, RegisterResponse
from ..schemas.errors import ApiError
from ..config import logger

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/register", response_model=RegisterResponse, responses={401: {"model": ApiError}}
)
async def register(
    form_data: RegisterFormData = Depends(),
    user_service: UserService = Depends(),
):
    user = user_service.get_user_by_username(form_data.username)
    if user:
        logger.error(f"Username already exists: {form_data.username}")
        raise HTTPException(status_code=401, detail="Username already exists")

    new_user = user_service.create_user(form_data)

    access_token = create_access_token(
        data={"sub": new_user.username, "id": new_user.id}
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post(
    "/login", response_model=LoginResponse, responses={401: {"model": ApiError}}
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(),
):
    user = user_service.get_user_by_username(form_data.username)
    if not user:
        logger.error(f"Incorrect username: {form_data.username}")
        raise HTTPException(status_code=401, detail="Incorrect username")
    if not user_service.verify_password(form_data.password, user.password):
        logger.error(f"Incorrect password for user: {user.username}")
        raise HTTPException(status_code=401, detail="Incorrect password")

    access_token = create_access_token(data={"sub": user.username, "id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
