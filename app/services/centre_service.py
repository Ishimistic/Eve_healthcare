from sqlalchemy.orm import Session

from app.models.diagnostic_centre import DiagnosticCentre
from app.repositories.centre_repository import CentreRepository
from app.schemas.centre import CentreCreate, CentreUpdate
from app.utils.pagination import paginate


centre_repository = CentreRepository()


def create_centre(
    db: Session,
    data: CentreCreate,
):
    centre = DiagnosticCentre(
        name=data.name,
        location=data.location,
    )

    centre_repository.create(db, centre)
    db.commit()
    db.refresh(centre)

    return centre


def get_centre(
    db: Session,
    centre_id: int,
):
    centre = centre_repository.get_by_id(
        db,
        centre_id,
    )

    if not centre:
        raise ValueError("Diagnostic centre not found")

    return centre


def list_centres(
    db: Session,
    page: int,
    page_size: int,
):
    stmt = centre_repository.get_all(db)

    return paginate(
        db,
        stmt,
        page,
        page_size,
    )


def update_centre(
    db: Session,
    centre_id: int,
    data: CentreUpdate,
):
    centre = get_centre(db, centre_id)

    if data.name is not None:
        centre.name = data.name

    if data.location is not None:
        centre.location = data.location

    if data.is_active is not None:
        centre.is_active = data.is_active

    db.commit()
    db.refresh(centre)

    return centre


def delete_centre(
    db: Session,
    centre_id: int,
):
    centre = get_centre(db, centre_id)

    centre.is_active = False

    db.commit()