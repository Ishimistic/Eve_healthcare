from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin
from app.db.session import get_db
from app.models.user import User
from app.schemas.test import (
    DiagnosticTestCreate,
    DiagnosticTestResponse,
    DiagnosticTestUpdate,
)
from app.services.test_service import (
    create_test,
    update_test,
    delete_test,
)


router = APIRouter(
    prefix="/admin/tests",
    tags=["Admin - Tests"],
)


@router.post(
    "/",
    response_model=DiagnosticTestResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(
    data: DiagnosticTestCreate,
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    return create_test(
        db,
        data,
    )


@router.patch(
    "/{test_id}",
    response_model=DiagnosticTestResponse,
)
def update(
    test_id: int,
    data: DiagnosticTestUpdate,
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    try:
        return update_test(
            db,
            test_id,
            data,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )


@router.delete(
    "/{test_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete(
    test_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    try:
        delete_test(
            db,
            test_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )