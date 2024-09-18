import contextlib
from typing import Any, AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

from .config import settings

Base = declarative_base()


class DatabaseSessionManager:
    def __init__(self, database_url: str, engine_kwargs: dict[str, Any] = {}):
        self._engine = create_async_engine(settings.database_url, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)

    async def close(self):
        """Dispose of the engine and clean up sessionmaker."""
        if self._engine:
            await self._engine.dispose()
            self._engine = None
            self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        """Open a new connection to the database."""
        if not self._engine:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.connect() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()  # Rollback on error
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        """Create a new asynchronous session."""
        if not self._sessionmaker:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._sessionmaker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()  # Rollback on error
                raise
            finally:
                # Sessions are automatically closed via async with
                pass  # This ensures session cleanup is handled


# Initialize the session manager with settings from app configuration
sessionmanager = DatabaseSessionManager(
    settings.database_url, {"echo": settings.echo_sql}
)


async def get_db_session() -> AsyncIterator[AsyncSession]:
    """Dependency function to retrieve a database session."""
    async with sessionmanager.session() as session:
        yield session
