from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.diagnostic_test import DiagnosticTest


class TestRepository:

    def get_by_id(
        self,
        db: Session,
        test_id: int,
    ):
        return db.get(
            DiagnosticTest,
            test_id,
        )

    def get_all(self):
        return select(
            DiagnosticTest
        ).order_by(
            DiagnosticTest.id
        )

    def create(
        self,
        db: Session,
        test: DiagnosticTest,
    ):
        db.add(test)
        db.flush()

        return test


test_repository = TestRepository()