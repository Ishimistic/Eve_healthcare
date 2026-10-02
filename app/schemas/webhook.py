from pydantic import BaseModel

from app.utils.enums import PaymentStatus


class PaymentWebhook(BaseModel):
    event_id: str
    payment_id: str
    status: PaymentStatus


class WebhookResponse(BaseModel):
    message: str
    event_id: str
    duplicate: bool