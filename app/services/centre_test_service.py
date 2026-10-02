from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.centre_test import CentreTest
from app.models.diagnostic_centre import DiagnosticCentre
from app.models.diagnostic_test import DiagnosticTest
from app.repositories.centre_test_repository import CentreTestRepository


centre_test_repository = CentreTestRepository()


def add_test_to_centre(
    db: Session,
    centre_id: int,
    test_id: int,
    price: Decimal,
):
    # Check centre exists
    centre = db.get(DiagnosticCentre, centre_id)

    if not centre:
        raise ValueError("Diagnostic centre not found")

    if not centre.is_active:
        raise ValueError("Diagnostic centre is inactive")

    # Check test exists
    test = db.get(DiagnosticTest, test_id)

    if not test:
        raise ValueError("Diagnostic test not found")

    if not test.is_active:
        raise ValueError("Diagnostic test is inactive")

    # Check whether this test is already offered by the centre
    existing = centre_test_repository.get_by_centre_and_test(
        db,
        centre_id,
        test_id,
    )

    if existing:
        raise ValueError("Test is already available at this centre")

    centre_test = CentreTest(
        centre_id=centre_id,
        test_id=test_id,
        price=price,
    )

    centre_test_repository.create(
        db,
        centre_test,
    )

    db.commit()
    db.refresh(centre_test)

    return centre_test


def update_centre_test(
    db: Session,
    centre_id: int,
    test_id: int,
    price: Decimal,
):
    centre_test = centre_test_repository.get_by_centre_and_test(
        db,
        centre_id,
        test_id,
    )

    if not centre_test:
        raise ValueError("Test is not available at this centre")

    centre_test.price = price

    db.commit()
    db.refresh(centre_test)

    return centre_test


def remove_test_from_centre(
    db: Session,
    centre_id: int,
    test_id: int,
):
    centre_test = centre_test_repository.get_by_centre_and_test(
        db,
        centre_id,
        test_id,
    )

    if not centre_test:
        raise ValueError("Test is not available at this centre")

    db.delete(centre_test)
    db.commit()