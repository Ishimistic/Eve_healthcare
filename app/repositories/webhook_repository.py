from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.webhook_event import WebhookEvent


class WebhookRepository:

    def get_by_event_id(
        self,
        db: Session,
        event_id: str,
    ):
        return db.scalar(
            select(WebhookEvent).where(
                WebhookEvent.event_id == event_id
            )
        )

    def create(
        self,
        db: Session,
        event: WebhookEvent,
    ):
        db.add(event)
        db.flush()

        return event