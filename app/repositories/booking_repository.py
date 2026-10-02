from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.utils.enums import BookingStatus


class BookingRepository:

    def get_by_id(
        self,
        db: Session,
        booking_id: int,
    ):
        return db.get(
            Booking,
            booking_id,
        )

    def get_user_bookings(
        self,
        db: Session,
        user_id: int,
    ):
        return select(
            Booking
        ).where(
            Booking.user_id == user_id
        ).order_by(
            Booking.created_at.desc()
        )

    def get_active_slot_booking(
        self,
        db: Session,
        centre_test_id: int,
        appointment_at,
    ):
        return db.scalar(
            select(Booking).where(
                Booking.centre_test_id == centre_test_id,
                Booking.appointment_at == appointment_at,
                Booking.status.in_(
                    [
                        BookingStatus.PENDING,
                        BookingStatus.CONFIRMED,
                    ]
                ),
            )
        )