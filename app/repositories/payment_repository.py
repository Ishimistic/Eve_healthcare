from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.payment import Payment


class PaymentRepository:

    def get_by_id(
        self,
        db: Session,
        payment_id: int,
    ):
        return db.get(
            Payment,
            payment_id,
        )

    def get_by_booking_id(
        self,
        db: Session,
        booking_id: int,
    ):
        return db.scalar(
            select(Payment).where(
                Payment.booking_id == booking_id
            )
        )

    def get_by_provider_id(
        self,
        db: Session,
        provider_payment_id: str,
    ):
        return db.scalar(
            select(Payment).where(
                Payment.provider_payment_id
                == provider_payment_id
            )
        )

    def create(
        self,
        db: Session,
        payment: Payment,
    ):
        db.add(payment)
        db.flush()

        return payment