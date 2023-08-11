from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from models import Base
from alembic import context

# Load database connection URL from Alembic configuration
config = context.config
db_url = config.get_main_option("sqlalchemy.url")

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set up your models' MetaData object here.
# Target_metadata is used for 'autogenerate' support.
target_metadata = Base.metadata

# Set up the SQLAlchemy engine using the provided database URL.
# We use pool.NullPool to avoid managing connections in Alembic.
engine = engine_from_config(
    config.get_section(config.config_ini_section),
    prefix="sqlalchemy.",
    url=db_url,
    poolclass=pool.NullPool
)


# Function to run migrations in 'offline' mode.
def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# Function to run migrations in 'online' mode.
def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


# Determine whether to run migrations in offline or online mode.
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
