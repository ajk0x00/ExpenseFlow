from fastapi import APIRouter
from app.api.v1.endpoints import accounts, transactions, statement_formats, categories, analytics

api_router = APIRouter()
api_router.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
api_router.include_router(statement_formats.router, prefix="/statement-formats", tags=["statement-formats"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])

from app.core.users import fastapi_users, auth_backend
from app.schemas.user import UserRead, UserCreate, UserUpdate

api_router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
api_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
api_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
