from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = "postgresql+asyncpg://postgres:12345@db:5432/postgres"
engine = create_async_engine(DATABASE_URL)
async_session_local = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass

async def get_db():
    async with async_session_local() as session:
        try:
            yield session
        finally:
            await session.close()
    

async def create_all():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)