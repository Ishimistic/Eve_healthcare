from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.webhook import (
    PaymentWebhook,
    WebhookResponse,
)
from app.services.webhook_service import (
    process_payment_webhook,
)


router = APIRouter(
    prefix="/payments",
    tags=["Payment Webhooks"],
)


@router.post(
    "/webhook/",
    response_model=WebhookResponse,
)
def payment_webhook(
    data: PaymentWebhook,
    db: Session = Depends(get_db),
):
    try:
        return process_payment_webhook(
            db,
            data.event_id,
            data.payment_id,
            data.status,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )