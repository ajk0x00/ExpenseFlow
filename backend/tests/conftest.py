import pytest
import pytest_asyncio
import asyncio
from typing import AsyncGenerator, Generator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.main import app
from app.db.session import get_db
import app.db.session as db_session_module
from app.core.config import settings

# Use in-memory SQLite for tests
# StaticPool is important for in-memory to share connection across threads/tasks if needed,
# though with async it is usually one thread.
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for each test session."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="function")
async def test_engine():
    engine = create_async_engine(
        TEST_DATABASE_URL, 
        connect_args={"check_same_thread": False}, 
        poolclass=StaticPool,
        echo=False
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest_asyncio.fixture(scope="function")
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    async_session_factory = sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session_factory() as session:
        yield session

@pytest_asyncio.fixture(scope="function")
async def client(db_session: AsyncSession, test_engine) -> AsyncGenerator[AsyncClient, None]:
    # Override get_db
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    
    # Patch AsyncSessionLocal used in startup to use our test engine/session factory
    # This prevents the startup event from connecting to the real DB
    original_session_local = db_session_module.AsyncSessionLocal
    test_session_factory = sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
    db_session_module.AsyncSessionLocal = test_session_factory

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
    
    # Restore
    db_session_module.AsyncSessionLocal = original_session_local
    app.dependency_overrides.clear()

@pytest_asyncio.fixture(scope="function")
async def test_user(client: AsyncClient, db_session: AsyncSession):
    """Create a test user and return credentials."""
    email = "testuser@example.com"
    password = "testpassword"
    
    # Register (or create directly in DB to be faster)
    # Using API to verify flow is good, but direct DB is faster.
    # Let's use API to implicitly test registration? No, stick to helpers for setup.
    # BUT, to test Auth, we should use API. For this fixture, just make sure user exists.
    
    from app.models.user import User
    # Note: access code internals like fast_hash_password logic if possible
    # Or just use the register endpoint.
    
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": password,
            "is_active": True,
            "is_superuser": False,
            "is_verified": True
        }
    )
    # If using in-memory DB, user won't exist yet, so this should succeed.
    if response.status_code == 400: # Already exists?
        pass

    return {"email": email, "password": password}

@pytest_asyncio.fixture(scope="function")
async def token_headers(client: AsyncClient, test_user):
    login_data = {
        "username": test_user["email"],
        "password": test_user["password"]
    }
    response = await client.post(
        "/api/v1/auth/jwt/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    data = response.json()
    access_token = data["access_token"]
    return {"Authorization": f"Bearer {access_token}"}
