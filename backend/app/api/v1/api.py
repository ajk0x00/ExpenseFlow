from fastapi import APIRouter
from app.api.v1.endpoints import accounts, transactions, statement_formats

api_router = APIRouter()
api_router.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
api_router.include_router(statement_formats.router, prefix="/statement-formats", tags=["statement-formats"])
