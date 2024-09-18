import asyncio
import os
from logging.config import fileConfig

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import Connection, pool
from sqlalchemy.ext.asyncio import create_async_engine

# Import your models and metadata
from app.core.database import Base
from app.models import PasswordResetToken, Task, users

# Load environment variables
load_dotenv()

# Alembic Config object, which provides access to the values within the .ini file
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata for 'autogenerate' support
target_metadata = Base.metadata


# Load the database URL from environment variables
def get_url():
    return os.getenv("DATABASE_URL")


# Offline migration function
def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = get_url()  # Get the database URL from env
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# Function to run migrations
def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


# Online migration function (async)
async def run_migrations_online():
    """Run migrations in 'online' mode."""
    # Create a configuration and set the DB URL
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()

    # Create an async engine
    connectable = create_async_engine(
        configuration["sqlalchemy.url"], poolclass=pool.NullPool
    )

    # Connect asynchronously and run migrations
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


# Determine if we're running migrations offline or online
if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
