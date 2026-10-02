from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.models.centre_test import CentreTest
from app.models.diagnostic_centre import DiagnosticCentre
from app.models.diagnostic_test import DiagnosticTest
from app.models.user import User
from app.repositories.booking_repository import (
    BookingRepository,
)
from app.utils.enums import BookingStatus
from app.utils.pagination import paginate


booking_repository = BookingRepository()


def create_booking(
    db: Session,
    user: User,
    centre_test_id: int,
    appointment_at,
):
    # Lock the CentreTest row for this transaction.
    #
    # This prevents two concurrent requests for the same
    # centre/test from both passing the availability check.
    centre_test = db.scalar(
        select(CentreTest)
        .where(CentreTest.id == centre_test_id)
        .with_for_update()
    )

    if not centre_test:
        raise ValueError(
            "Centre-test relationship not found"
        )

    centre = db.get(
        DiagnosticCentre,
        centre_test.centre_id,
    )

    test = db.get(
        DiagnosticTest,
        centre_test.test_id,
    )

    if not centre or not centre.is_active:
        raise ValueError(
            "Diagnostic centre is inactive"
        )

    if not test or not test.is_active:
        raise ValueError(
            "Diagnostic test is inactive"
        )

    existing_booking = (
        booking_repository.get_active_slot_booking(
            db,
            centre_test_id,
            appointment_at,
        )
    )

    if existing_booking:
        raise ValueError(
            "Appointment slot is already booked"
        )

    booking = Booking(
        user_id=user.id,
        centre_test_id=centre_test.id,
        appointment_at=appointment_at,
        amount=centre_test.price,
        status=BookingStatus.PENDING,
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)

    return booking


def get_booking(
    db: Session,
    booking_id: int,
):
    booking = booking_repository.get_by_id(
        db,
        booking_id,
    )

    if not booking:
        raise ValueError(
            "Booking not found"
        )

    return booking


def list_user_bookings(
    db: Session,
    user_id: int,
    page: int,
    page_size: int,
):
    stmt = booking_repository.get_user_bookings(
        db,
        user_id,
    )

    return paginate(
        db,
        stmt,
        page,
        page_size,
    )


def cancel_booking(
    db: Session,
    booking_id: int,
    user: User,
):
    booking = get_booking(
        db,
        booking_id,
    )

    if (
        booking.user_id != user.id
        and user.role.value != "ADMIN"
    ):
        raise PermissionError(
            "You are not allowed to modify this booking"
        )

    if booking.status == BookingStatus.CANCELLED:
        raise ValueError(
            "Booking is already cancelled"
        )

    if booking.status == BookingStatus.FAILED:
        raise ValueError(
            "Failed booking cannot be cancelled"
        )

    booking.status = BookingStatus.CANCELLED

    db.commit()
    db.refresh(booking)

    return booking