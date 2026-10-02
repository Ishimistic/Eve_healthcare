from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict
from app.utils.enums import PaymentStatus


class PaymentCreate(BaseModel):
    booking_id: int
    simulate_status: PaymentStatus


class PaymentResponse(BaseModel):
    id: int
    booking_id: int
    provider_payment_id: str
    amount: Decimal
    status: PaymentStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)