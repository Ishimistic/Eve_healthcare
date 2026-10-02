from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.centre_test import CentreTest


class CentreTestRepository:

    def get_by_id(
        self,
        db: Session,
        centre_test_id: int,
    ):
        return db.get(
            CentreTest,
            centre_test_id,
        )

    def get_by_centre_and_test(
        self,
        db: Session,
        centre_id: int,
        test_id: int,
    ):
        return db.scalar(
            select(CentreTest).where(
                CentreTest.centre_id == centre_id,
                CentreTest.test_id == test_id,
            )
        )

    def create(
        self,
        db: Session,
        centre_test: CentreTest,
    ):
        db.add(centre_test)
        db.flush()

        return centre_test