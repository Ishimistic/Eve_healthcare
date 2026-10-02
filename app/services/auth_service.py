from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    hash_refresh_token,
    verify_password,
    decode_refresh_token,
)

from app.models.refresh_token import RefreshToken
from app.repositories.refresh_token_repository import (
    RefreshTokenRepository,
)

from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.schemas.auth import UserRegister



refresh_token_repository = RefreshTokenRepository()



def register_user(
    db: Session,
    data: UserRegister,
) -> User:

    existing_user = db.scalar(
        select(User).where(User.email == data.email)
    )

    if existing_user:
        raise ValueError("Email already registered")

    user = User(
        name=data.name,
        email=data.email,
        password_hash=hash_password(data.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user



def login_user(db: Session, email: str, password: str):
    user = db.scalar(
        select(User).where(User.email == email)
    )

    if not user:
        raise ValueError("Invalid email or password")

    if not verify_password(
        password,
        user.password_hash,
    ):
        raise ValueError("Invalid email or password")

    if not user.is_active:
        raise ValueError("User account is inactive")

    access_token = create_access_token(user.id)

    refresh_token, expires_at = create_refresh_token(
        user.id
    )

    refresh_token_record = RefreshToken(
        user_id=user.id,
        token_hash=hash_refresh_token(refresh_token),
        expires_at=expires_at,
    )

    db.add(refresh_token_record)
    db.commit()

    return user, access_token, refresh_token


def refresh_tokens(
    db: Session,
    raw_refresh_token: str,
):
    try:
        payload = decode_refresh_token(raw_refresh_token)
    except Exception:
        raise ValueError("Invalid or expired refresh token")

    user_id = payload.get("sub")

    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        raise ValueError("Invalid refresh token")

    token_hash = hash_refresh_token(raw_refresh_token)

    stored_token = refresh_token_repository.get_by_hash(
        db,
        token_hash,
    )

    if not stored_token:
        raise ValueError("Refresh token not found")

    if stored_token.revoked_at is not None:
        raise ValueError("Refresh token has been revoked")

    if stored_token.expires_at <= datetime.now(timezone.utc):
        raise ValueError("Refresh token has expired")

    user = db.get(User, user_id)

    if not user:
        raise ValueError("User not found")

    if not user.is_active:
        raise ValueError("User account is inactive")

    # Revoke the old refresh token
    refresh_token_repository.revoke(
        db,
        stored_token,
    )

    # Create new tokens
    new_access_token = create_access_token(user.id)

    new_refresh_token, expires_at = create_refresh_token(
        user.id
    )

    new_refresh_token_record = RefreshToken(
        user_id=user.id,
        token_hash=hash_refresh_token(new_refresh_token),
        expires_at=expires_at,
    )

    refresh_token_repository.create(
        db,
        new_refresh_token_record,
    )

    db.commit()

    return (
        user,
        new_access_token,
        new_refresh_token,
    )
    
    
def logout_user(
    db: Session,
    raw_refresh_token: str,
):
    token_hash = hash_refresh_token(
        raw_refresh_token
    )

    stored_token = refresh_token_repository.get_by_hash(
        db,
        token_hash,
    )

    if not stored_token:
        raise ValueError("Refresh token not found")

    if stored_token.revoked_at is not None:
        return

    refresh_token_repository.revoke(
        db,
        stored_token,
    )

    db.commit()