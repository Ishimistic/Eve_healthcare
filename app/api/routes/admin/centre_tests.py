from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin
from app.db.session import get_db
from app.models.user import User
from app.schemas.centre_test import (
    CentreTestCreate,
    CentreTestResponse,
    CentreTestUpdate,
)
from app.services.centre_test_service import (
    add_test_to_centre,
    update_centre_test,
    remove_test_from_centre,
)


router = APIRouter(
    prefix="/admin/centres",
    tags=["Admin - Centre Tests"],
)


@router.post(
    "/{centre_id}/tests/",
    response_model=CentreTestResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_test(
    centre_id: int,
    data: CentreTestCreate,
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    try:
        return add_test_to_centre(
            db,
            centre_id,
            data.test_id,
            data.price,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        )


@router.patch(
    "/{centre_id}/tests/{test_id}/",
    response_model=CentreTestResponse,
)
def update_test_price(
    centre_id: int,
    test_id: int,
    data: CentreTestUpdate,
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    try:
        return update_centre_test(
            db,
            centre_id,
            test_id,
            data.price,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )


@router.delete(
    "/{centre_id}/tests/{test_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_test(
    centre_id: int,
    test_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    try:
        remove_test_from_centre(
            db,
            centre_id,
            test_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )