from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.models.payment import Payment
from app.models.webhook_event import WebhookEvent
from app.repositories.webhook_repository import (
    WebhookRepository,
)
from app.utils.enums import (
    BookingStatus,
    PaymentStatus,
)


webhook_repository = WebhookRepository()


def process_payment_webhook(
    db: Session,
    event_id: str,
    provider_payment_id: str,
    status: PaymentStatus,
):
    existing_event = (
        webhook_repository.get_by_event_id(
            db,
            event_id,
        )
    )

    if existing_event:
        return {
            "message": "Webhook already processed",
            "event_id": event_id,
            "duplicate": True,
        }

    payment = db.scalar(
        select(Payment).where(
            Payment.provider_payment_id
            == provider_payment_id
        )
    )

    if not payment:
        raise ValueError(
            "Payment not found"
        )

    # Try to register the event.
    #
    # event_id is UNIQUE in PostgreSQL, so even concurrent
    # webhook requests cannot both successfully create it.
    event = WebhookEvent(
        event_id=event_id,
        payment_id=payment.id,
        status=status.value,
    )

    try:
        webhook_repository.create(
            db,
            event,
        )

    except IntegrityError:
        db.rollback()

        return {
            "message": "Webhook already processed",
            "event_id": event_id,
            "duplicate": True,
        }

    booking = db.get(
        Booking,
        payment.booking_id,
    )

    if not booking:
        db.rollback()
        raise ValueError(
            "Related booking not found"
        )

    # Don't allow a webhook to move a terminal payment
    # into a contradictory state.
    if (
        payment.status != status
        and payment.status in [
            PaymentStatus.SUCCESS,
            PaymentStatus.FAILED,
        ]
    ):
        db.rollback()

        raise ValueError(
            "Payment is already in a final state"
        )

    payment.status = status

    if status == PaymentStatus.SUCCESS:
        booking.status = BookingStatus.CONFIRMED
    else:
        booking.status = BookingStatus.FAILED

    db.commit()

    return {
        "message": "Webhook processed successfully",
        "event_id": event_id,
        "duplicate": False,
    }