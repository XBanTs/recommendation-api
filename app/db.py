from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# Use SQLite instead of PostgreSQL
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./movies.db"

# Create async engine for SQLite
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, echo=True, future=True
)

# Async session
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

# Base class for models
Base = declarative_base()

# Dependency for getting DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# Initialize DB (create tables)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("Tables found in metadata:", Base.metadata.tables.keys())
