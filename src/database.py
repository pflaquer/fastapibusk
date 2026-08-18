import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# On Render, the database URL is provided as an environment variable
# We replace postgres:// with postgresql+asyncpg:// to force async mode
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:pass@localhost/dbname")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)

# The async engine manages our connection pool to the database
engine = create_async_engine(DATABASE_URL, pool_size=20, max_overflow=10)

# A session factory for generating transient async sessions per web request
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

# Dependency to safely inject and close database connections per web request
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
