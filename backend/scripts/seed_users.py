import asyncio

from app.database import AsyncSessionLocal
from app.orm_models import User, ROLE
from app.security import encrypt_password

async def seed_users() -> None:
    async with AsyncSessionLocal() as session:
        session.add_all([
            User(username="admin", hashed_password=encrypt_password("AdminPass123!"), role=ROLE.OPERATIONS_ADMIN),
            User(username="technician", hashed_password=encrypt_password("TechnicianPass123!"), role=ROLE.FIELD_TECHNICIAN),
            User(username="auditor", hashed_password=encrypt_password("AuditorPass123!"), role=ROLE.AUDITOR),
        ])
        await session.commit()

if __name__ == "__main__":
    asyncio.run(seed_users())