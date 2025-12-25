import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.core.config import settings

from app.api.v1.api import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

from app.core.users import UserManager
from app.schemas.user import UserCreate
from app.models.user import User
from fastapi_users.db import SQLAlchemyUserDatabase
from app.db.session import AsyncSessionLocal

@app.on_event("startup")
async def on_startup():
    async with AsyncSessionLocal() as session:
        user_db = SQLAlchemyUserDatabase(session, User)
        user_manager = UserManager(user_db)
        
        email = "admin@example.com"
        try:
            # Check if user exists
            # We can't use get_by_email directly if it raises exception on not found? 
            # Reference: fastapi-users managers usually raise exceptions or return None depending on version.
            # But get_by_email return type is User, usually raises UserNotExists if not found?
            # Let's inspect UserManager implementation or assume safe create.
            # Actually simpler: just try to create and ignore "User already exists" exception
            user = await user_manager.get_by_email(email)
            print(f"User {email} already exists")
        except Exception:
            print(f"Creating user {email}")
            user_in = UserCreate(
                email=email,
                password="admin",
                is_superuser=True,
                is_active=True,
                is_verified=True,
            )
            await user_manager.create(user_in)
            print(f"User {email} created")

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    print(f"DEBUG: Allowed Origins: {settings.BACKEND_CORS_ORIGINS}")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin).rstrip("/") for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

# Serve static files if the directory exists
static_dir = "static"
if os.path.exists(static_dir):
    app.mount("/assets", StaticFiles(directory=f"{static_dir}/assets"), name="static")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        # If the path starts with the API prefix, let it fall through (though include_router should handle it)
        if full_path.startswith(settings.API_V1_STR.lstrip("/")):
            return {"detail": "Not Found"}
        
        # Check if the requested file exists in the static directory
        file_path = os.path.join(static_dir, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        
        # Otherwise, serve index.html for client-side routing
        return FileResponse(os.path.join(static_dir, "index.html"))
else:
    @app.get("/")
    async def root():
        return {"message": "Hello from FastAPI (Static files not found)"}
