from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.diagnostic_centre import DiagnosticCentre


class CentreRepository:

    def get_by_id(
        self,
        db: Session,
        centre_id: int,
    ) -> DiagnosticCentre | None:
        return db.get(DiagnosticCentre, centre_id)

    def get_active_by_id(
        self,
        db: Session,
        centre_id: int,
    ) -> DiagnosticCentre | None:
        return db.scalar(
            select(DiagnosticCentre).where(
                DiagnosticCentre.id == centre_id,
                DiagnosticCentre.is_active.is_(True),
            )
        )

    def get_all(self, db: Session):
        return select(
            DiagnosticCentre
        ).order_by(
            DiagnosticCentre.id
        )

    def create(
        self,
        db: Session,
        centre: DiagnosticCentre,
    ):
        db.add(centre)
        db.flush()
        return centre

    def delete(
        self,
        db: Session,
        centre: DiagnosticCentre,
    ):
        db.delete(centre)