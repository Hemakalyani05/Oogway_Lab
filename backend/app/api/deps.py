"""
API Dependency Injections.
"""
from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.core.config import settings

# Re-export get_db for route dependencies
__all__ = ["get_db", "settings"]
