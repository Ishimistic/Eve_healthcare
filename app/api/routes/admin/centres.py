from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin
from app.db.session import get_db
from app.models.user import User
from app.schemas.centre import (
    CentreCreate,
    CentreResponse,
    CentreUpdate,
)
from app.services.centre_service import (
    create_centre,
    update_centre,
    delete_centre,
)


router = APIRouter(
    prefix="/admin/centres",
    tags=["Admin - Centres"],
)


@router.post(
    "/",
    response_model=CentreResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(
    data: CentreCreate,
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    return create_centre(db, data)


@router.patch(
    "/{centre_id}",
    response_model=CentreResponse,
)
def update(
    centre_id: int,
    data: CentreUpdate,
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    try:
        return update_centre(
            db,
            centre_id,
            data,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )


@router.delete(
    "/{centre_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete(
    centre_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    try:
        delete_centre(
            db,
            centre_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )