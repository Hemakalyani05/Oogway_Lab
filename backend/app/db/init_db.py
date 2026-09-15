"""
Database schema initialization and table creation.
"""
from app.db.session import Base, is_async_driver
from app.core.logging import logger


async def init_database():
    """Creates database tables if they do not exist."""
    try:
        if is_async_driver:
            from app.db.session import async_engine
            async with async_engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
        else:
            from app.db.session import engine
            Base.metadata.create_all(bind=engine)
        logger.info("Database schema initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing database schema: {e}")
        raise
