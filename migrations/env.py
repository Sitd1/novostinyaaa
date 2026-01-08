import os
import sys
from logging.config import fileConfig

from sqlalchemy import pool

from alembic import context
from shared.database.models import Base
from shared.config.base_configs.database_config import database_config

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import pool, create_engine

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata


def get_url():
    user = os.getenv("DB_USER", "postgres").strip().replace('"', '')
    password = os.getenv("DB_PASSWORD", "postgres").strip().replace('"', '')
    host = os.getenv("DB_HOST", "db").strip().replace('"', '')
    port = os.getenv("DB_PORT", "5432").strip().replace('"', '')
    db = os.getenv("DB_NAME", "novostinya_db").strip().replace('"', '')

    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
    # return database_config.url_psycopg

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connect_url = get_url()
    print(f"CONNECTING TO: {connect_url}") # Добавь этот принт, увидим его в консоли

    from sqlalchemy import create_engine
    connectable = create_engine(
        connect_url,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
