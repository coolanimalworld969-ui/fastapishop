import asyncio
from logging.config import fileConfig

from sqlalchemy import pool

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine
from config import DB_SETTINGS
from models import *

config = context.config


if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", DB_SETTINGS.async_url + "?async_fallback=True")

target_metadata = Base.metadata



def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_server_default=True
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_server_default=True
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    # Заменяем engine_from_config на создание асинхронного движка
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool
    )

    # Здесь async with использовать МОЖНО, так как движок асинхронный
    async with connectable.connect() as connection:
        # Передаем управление синхронной функции через run_sync
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
