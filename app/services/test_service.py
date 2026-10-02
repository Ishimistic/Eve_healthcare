from sqlalchemy.orm import Session

from app.models.diagnostic_test import DiagnosticTest
from app.repositories.test_repository import test_repository
from app.schemas.test import (
    DiagnosticTestCreate,
    DiagnosticTestUpdate,
)
from app.utils.pagination import paginate


def create_test(
    db: Session,
    data: DiagnosticTestCreate,
):
    diagnostic_test = DiagnosticTest(
        name=data.name,
        description=data.description,
    )

    test_repository.create(
        db,
        diagnostic_test,
    )

    db.commit()
    db.refresh(diagnostic_test)

    return diagnostic_test


def get_test(
    db: Session,
    test_id: int,
):
    diagnostic_test = test_repository.get_by_id(
        db,
        test_id,
    )

    if not diagnostic_test:
        raise ValueError(
            "Diagnostic test not found"
        )

    return diagnostic_test


def list_tests(
    db: Session,
    page: int,
    page_size: int,
):
    stmt = test_repository.get_all()

    return paginate(
        db,
        stmt,
        page,
        page_size,
    )


def update_test(
    db: Session,
    test_id: int,
    data: DiagnosticTestUpdate,
):
    diagnostic_test = get_test(
        db,
        test_id,
    )

    if data.name is not None:
        diagnostic_test.name = data.name

    if data.description is not None:
        diagnostic_test.description = data.description

    if data.is_active is not None:
        diagnostic_test.is_active = data.is_active

    db.commit()
    db.refresh(diagnostic_test)

    return diagnostic_test


def delete_test(
    db: Session,
    test_id: int,
):
    diagnostic_test = get_test(
        db,
        test_id,
    )

    diagnostic_test.is_active = False

    db.commit()