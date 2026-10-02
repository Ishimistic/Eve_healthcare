from math import ceil

from sqlalchemy import func, select
from sqlalchemy.orm import Session


def paginate(
    db: Session,
    stmt,
    page: int,
    page_size: int,
):
    count_stmt = select(
        func.count()
    ).select_from(
        stmt.order_by(None).subquery()
    )

    total = db.scalar(count_stmt) or 0

    items = db.scalars(
        stmt
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).all()

    pages = ceil(total / page_size) if total else 0

    return {
        "items": items,
        "page": page,
        "page_size": page_size,
        "total": total,
        "pages": pages,
    }