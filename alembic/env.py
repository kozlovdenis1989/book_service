from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from app.db import Base  
from app.models import Reservation, Table  
   
# Эта строка для настройки логирования
fileConfig(context.config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline():
   """Run migrations in 'offline' mode."""
   url = context.config.get_main_option("sqlalchemy.url")
   context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

   with context.begin_transaction():
       context.run_migrations()

def run_migrations_online():
   """Run migrations in 'online' mode."""
   connectable = engine_from_config(
       context.config.get_section(context.config.config_ini_section),
       prefix='sqlalchemy.',
       poolclass=pool.NullPool,
   )

   with connectable.connect() as connection:
       context.configure(
           connection=connection,
           target_metadata=target_metadata,
       )

       with context.begin_transaction():
           context.run_migrations()

if context.is_offline_mode():
   run_migrations_offline()
else:
   run_migrations_online()

# # Подключение к базе данных
# def get_url():
#     return DATABASE_URL