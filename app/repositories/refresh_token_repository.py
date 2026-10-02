from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.refresh_token import RefreshToken


class RefreshTokenRepository:

    def get_by_hash(
        self,
        db: Session,
        token_hash: str,
    ) -> RefreshToken | None:
        return db.scalar(
            select(RefreshToken).where(
                RefreshToken.token_hash == token_hash
            )
        )

    def revoke(
        self,
        db: Session,
        refresh_token: RefreshToken,
    ) -> None:
        refresh_token.revoked_at = datetime.now(timezone.utc)

    def create(
        self,
        db: Session,
        refresh_token: RefreshToken,
    ) -> RefreshToken:
        db.add(refresh_token)
        db.flush()
        return refresh_token