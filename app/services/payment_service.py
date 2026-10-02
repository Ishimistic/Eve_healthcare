from uuid import uuid4

from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.models.payment import Payment
from app.models.user import User
from app.repositories.payment_repository import (
    PaymentRepository,
)
from app.utils.enums import (
    BookingStatus,
    PaymentStatus,
)


payment_repository = PaymentRepository()


def process_payment(
    db: Session,
    booking_id: int,
    simulated_status: PaymentStatus,
    user: User,
):
    booking = db.get(
        Booking,
        booking_id,
    )

    if not booking:
        raise ValueError(
            "Booking not found"
        )

    if (
        booking.user_id != user.id
        and user.role.value != "ADMIN"
    ):
        raise PermissionError(
            "You are not allowed to pay for this booking"
        )

    if booking.status != BookingStatus.PENDING:
        raise ValueError(
            "Payment can only be processed for a pending booking"
        )

    existing_payment = (
        payment_repository.get_by_booking_id(
            db,
            booking_id,
        )
    )

    if existing_payment:
        return existing_payment

    provider_payment_id = (
        f"pay_{uuid4().hex}"
    )

    payment = Payment(
        booking_id=booking.id,
        provider_payment_id=provider_payment_id,
        amount=booking.amount,
        status=simulated_status,
    )

    payment_repository.create(
        db,
        payment,
    )

    if simulated_status == PaymentStatus.SUCCESS:
        booking.status = BookingStatus.CONFIRMED

    else:
        booking.status = BookingStatus.FAILED

    db.commit()
    db.refresh(payment)

    return payment


def get_payment(
    db: Session,
    payment_id: int,
    user: User,
):
    payment = payment_repository.get_by_id(
        db,
        payment_id,
    )

    if not payment:
        raise ValueError(
            "Payment not found"
        )

    if (
        payment.booking.user_id != user.id
        and user.role.value != "ADMIN"
    ):
        raise PermissionError(
            "You are not allowed to view this payment"
        )

    return payment