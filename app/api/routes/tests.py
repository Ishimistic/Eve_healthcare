from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.common import PaginatedResponse
from app.schemas.test import DiagnosticTestResponse
from app.services.test_service import (
    get_test,
    list_tests,
)


router = APIRouter(
    prefix="/tests",
    tags=["Diagnostic Tests"],
)


@router.get(
    "/",
    response_model=PaginatedResponse[DiagnosticTestResponse],
)
def get_tests(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return list_tests(
        db,
        page,
        page_size,
    )


@router.get(
    "/{test_id}",
    response_model=DiagnosticTestResponse,
)
def get_test_by_id(
    test_id: int,
    db: Session = Depends(get_db),
):
    try:
        return get_test(
            db,
            test_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )