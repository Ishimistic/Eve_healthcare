from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Numeric,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class CentreTest(Base):
    __tablename__ = "centre_tests"

    __table_args__ = (
        UniqueConstraint(
            "centre_id",
            "test_id",
            name="uq_centre_test",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    centre_id: Mapped[int] = mapped_column(
        ForeignKey("diagnostic_centres.id"),
        nullable=False,
    )

    test_id: Mapped[int] = mapped_column(
        ForeignKey("diagnostic_tests.id"),
        nullable=False,
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    centre = relationship(
        "DiagnosticCentre",
        back_populates="tests",
    )

    test = relationship(
        "DiagnosticTest",
        back_populates="centres",
    )

    bookings = relationship(
        "Booking",
        back_populates="centre_test",
    )