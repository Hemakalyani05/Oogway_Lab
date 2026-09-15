"""
Database session management and query execution helper supporting standard SQLite and PostgreSQL.
"""
from typing import AsyncGenerator, Any
import inspect
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

from app.core.config import settings
from app.core.logging import logger

Base = declarative_base()

db_url = settings.DATABASE_URL
is_async_driver = "+asyncpg" in db_url

if is_async_driver:
    from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
    async_engine = create_async_engine(db_url, echo=False, future=True)
    AsyncSessionLocal = async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False
    )
    
    async def get_db() -> AsyncGenerator[Any, None]:
        async with AsyncSessionLocal() as session:
            try:
                yield session
            except Exception as e:
                await session.rollback()
                logger.error(f"Database session error: {e}")
                raise
            finally:
                await session.close()
else:
    sync_url = db_url.replace("+aiosqlite", "")
    if sync_url.startswith("sqlite:///"):
        engine = create_engine(sync_url, connect_args={"check_same_thread": False}, echo=False)
    else:
        engine = create_engine(sync_url, echo=False)
        
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    async def get_db() -> AsyncGenerator[Any, None]:
        db = SessionLocal()
        try:
            yield db
        except Exception as e:
            db.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            db.close()


async def db_execute(db: Any, stmt: Any) -> Any:
    """Executes a statement whether db is AsyncSession or standard Session."""
    res = db.execute(stmt)
    if inspect.isawaitable(res):
        return await res
    return res


async def db_commit(db: Any) -> None:
    """Commits whether db is AsyncSession or standard Session."""
    res = db.commit()
    if inspect.isawaitable(res):
        await res


async def db_refresh(db: Any, obj: Any) -> None:
    """Refreshes whether db is AsyncSession or standard Session."""
    res = db.refresh(obj)
    if inspect.isawaitable(res):
        await res


async def db_delete(db: Any, obj: Any) -> None:
    """Deletes whether db is AsyncSession or standard Session."""
    res = db.delete(obj)
    if inspect.isawaitable(res):
        await res
