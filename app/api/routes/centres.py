from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.centre import (
    CentreResponse,
)
from app.schemas.common import PaginatedResponse
from app.services.centre_service import (
    get_centre,
    list_centres,
)


router = APIRouter(
    prefix="/centres",
    tags=["Diagnostic Centres"],
)


@router.get(
    "/",
    response_model=PaginatedResponse[CentreResponse],
)
def get_centres(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return list_centres(
        db,
        page,
        page_size,
    )


@router.get(
    "/{centre_id}",
    response_model=CentreResponse,
)
def get_centre_by_id(
    centre_id: int,
    db: Session = Depends(get_db),
):
    try:
        return get_centre(
            db,
            centre_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )