# import os
from app.config import settings
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

DATABASE_URL = settings.database_url
"""
os.environ.get(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:Lact0seFr33@cashcow-2478.ctagwcmes3hh.us-east-2.rds.amazonaws.com:5432/cashcow",
)
"""

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)