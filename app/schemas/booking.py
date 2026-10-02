from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict
from app.utils.enums import BookingStatus


class BookingCreate(BaseModel):
    centre_test_id: int
    appointment_at: datetime


class BookingResponse(BaseModel):
    id: int
    user_id: int
    centre_test_id: int
    appointment_at: datetime
    amount: Decimal
    status: BookingStatus
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )