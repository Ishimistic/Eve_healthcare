from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    UserRegister,
    RefreshTokenRequest,
    TokenResponse,
)
from app.schemas.user import UserResponse
from app.services.auth_service import (
    login_user,
    register_user,
    refresh_tokens,
    logout_user,
)
from app.core.dependencies import get_current_user


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    data: UserRegister,
    db: Session = Depends(get_db),
):
    try:
        return register_user(db, data)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        )
        
        
@router.post(
    "/login",
    response_model=LoginResponse,
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
):
    try:
        user, access_token, refresh_token = login_user(
            db,
            data.email,
            data.password,
        )

        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user=user,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        )
        
        
@router.post(
    "/refresh",
    response_model=TokenResponse,
)
def refresh(
    data: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    try:
        (
            _user,
            access_token,
            refresh_token,
        ) = refresh_tokens(
            db,
            data.refresh_token,
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        )
        
        
@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user



@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
)
def logout(
    data: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    try:
        logout_user(
            db,
            data.refresh_token,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        )