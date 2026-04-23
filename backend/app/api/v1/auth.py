from fastapi import APIRouter, HTTPException, status
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from pydantic import BaseModel, EmailStr

from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    route_class=DishkaRoute,
)


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    body: RegisterRequest,
    service: FromDishka[AuthService],
) -> TokenResponse:
    try:
        await service.register(email=body.email, password=body.password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    token = await service.login(email=body.email, password=body.password)
    return TokenResponse(access_token=token)


@router.post("/login")
async def login(
    body: LoginRequest,
    service: FromDishka[AuthService],
) -> TokenResponse:
    try:
        token = await service.login(email=body.email, password=body.password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    return TokenResponse(access_token=token)
