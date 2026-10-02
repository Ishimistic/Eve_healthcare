from fastapi import APIRouter

from app.api.routes.auth import router as auth_router
from app.api.routes.centres import router as centres_router
from app.api.routes.tests import router as tests_router
from app.api.routes.bookings import router as bookings_router
from app.api.routes.payments import router as payments_router
from app.api.routes.webhooks import router as webhooks_router

from app.api.routes.admin.centres import (
    router as admin_centres_router,
)
from app.api.routes.admin.tests import (
    router as admin_tests_router,
)
from app.api.routes.admin.centre_tests import (
    router as admin_centre_tests_router,
)


api_router = APIRouter(
    prefix="/api/v1",
)


# Authentication
api_router.include_router(
    auth_router
)


# Public/user APIs
api_router.include_router(
    centres_router
)

api_router.include_router(
    tests_router
)

api_router.include_router(
    bookings_router
)

api_router.include_router(
    payments_router
)

api_router.include_router(
    webhooks_router
)


# Admin APIs
api_router.include_router(
    admin_centres_router
)

api_router.include_router(
    admin_tests_router
)

api_router.include_router(
    admin_centre_tests_router
)