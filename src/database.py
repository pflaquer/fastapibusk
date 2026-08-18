import os
import sys
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# Attempt to load the connection string from Render's dashboard environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("\n❌ ERROR: DATABASE_URL environment variable is missing in Render dashboard!", file=sys.stderr)
    print("Please go to the Environment tab of your Web Service and add it.\n", file=sys.stderr)
    # Temporary fallback to keep the app from crashing on start if the variable isn't ready
    DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Convert default Render postgres string format to asyncpg format automatically
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)

# Add SSL requirements for Render's cloud connection
connect_args = {}
if "render.com" in DATABASE_URL or "ondigitalocean" in DATABASE_URL:
    connect_args = {"ssl": "require"}

# Construct the asynchronous database engine
engine = create_async_engine(
    DATABASE_URL, 
    pool_size=20, 
    max_overflow=10,
    connect_args=connect_args
)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
