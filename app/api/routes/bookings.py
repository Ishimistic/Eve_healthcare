from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.booking import (
    BookingCreate,
    BookingResponse,
)
from app.schemas.common import PaginatedResponse
from app.services.booking_service import (
    cancel_booking,
    create_booking,
    get_booking,
    list_user_bookings,
)


router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)


@router.post(
    "/",
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(
    data: BookingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return create_booking(
            db,
            current_user,
            data.centre_test_id,
            data.appointment_at,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        )


@router.get(
    "/",
    response_model=PaginatedResponse[BookingResponse],
)
def get_my_bookings(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return list_user_bookings(
        db,
        current_user.id,
        page,
        page_size,
    )


@router.get(
    "/{booking_id}/",
    response_model=BookingResponse,
)
def get_by_id(
    booking_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        booking = get_booking(
            db,
            booking_id,
        )

        if (
            booking.user_id != current_user.id
            and current_user.role.value != "ADMIN"
        ):
            raise PermissionError(
                "You are not allowed to view this booking"
            )

        return booking

    except PermissionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )


@router.patch(
    "/{booking_id}/cancel/",
    response_model=BookingResponse,
)
def cancel(
    booking_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return cancel_booking(
            db,
            booking_id,
            current_user,
        )

    except PermissionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        )