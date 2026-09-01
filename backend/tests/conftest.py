import os
import pytest_asyncio

from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.dependencies import get_db
from app.main import app
from app.orm_models import Base, Branch, User, ROLE, Service_Call, SERVICE_CALL_STATUS, SERVICE_CALL_PRIORITY, Technician, ATM, ATM_STATUS
from app.security import create_access_token, encrypt_password

TEST_DATABASE_URL = os.environ.get(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://postgres:L%40ctoseFr33@127.0.0.1:5432/cashcow_test"
)

# This session is for tests only.
test_engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
TestSessionLocal = async_sessionmaker(test_engine, expire_on_commit=False)

@pytest_asyncio.fixture
async def db_session():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestSessionLocal() as session:
        yield session

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()

@pytest_asyncio.fixture
async def seeded_users(db_session):
    users = {
        "admin": User(username="test_admin", hashed_password=encrypt_password("pw"), role=ROLE.OPERATIONS_ADMIN),
        "technician": User(username="test_technician", hashed_password=encrypt_password("pw"), role=ROLE.FIELD_TECHNICIAN),
        "auditor": User(username="test_auditor", hashed_password=encrypt_password("pw"), role=ROLE.AUDITOR),
    }
    for user in users.values():
        db_session.add(user)
    await db_session.commit()
    for user in users.values():
        await db_session.refresh(user)
    return users

@pytest_asyncio.fixture
async def seeded_branch(db_session):
    branch = Branch(name="Test Branch", location_region="Test Region", capacity=10, supervisor_id=1)
    db_session.add(branch)
    await db_session.commit()
    await db_session.refresh(branch)
    return branch

@pytest_asyncio.fixture
async def seeded_service_call(db_session, seeded_branch):
    atm = ATM(
        serial_num="Test-Serial",
        model="Test-Model",
        cash_lvl = 7500,
        branch_id = seeded_branch.id,
        status=ATM_STATUS.OPERATIONAL,
    )
    technician = Technician(name="Test-Technician", branch_id=seeded_branch.id)
    db_session.add_all([atm, technician])
    await db_session.commit()
    await db_session.refresh(atm)
    await db_session.refresh(technician)

    service_call = Service_Call(
        title="Test Service_Call",
        priority=SERVICE_CALL_PRIORITY.LOW,
        status=SERVICE_CALL_STATUS.PENDING,
        atm_id=atm.id,
        technician_id=technician.id,
    )
    db_session.add(service_call)
    await db_session.commit()
    await db_session.refresh(service_call)
    return service_call

def auth_header(user: User) -> dict[str, str]:
    token = create_access_token(data={"sub": user.username, "role": user.role.value})
    return {"Authorization" : f"Bearer {token}"}