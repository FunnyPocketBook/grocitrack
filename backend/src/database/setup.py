from sqlalchemy import create_engine, text
from config import Config
from database.model import Base
import time


config = Config()
engine = create_engine(
    f"postgresql+psycopg://{config.get('database')['username']}:{config.get('database')['password']}@{config.get('database')['host']}/{config.get('database')['database_name']}",
    pool_size=20,
    max_overflow=10,
)

attempts = 0
while attempts < 5:
    try:
        Base.metadata.create_all(engine)
        break
    except Exception:
        attempts += 1
        time.sleep(5)


sql_setup_statements = [
    "CREATE EXTENSION IF NOT EXISTS pg_trgm;",
    "CREATE INDEX IF NOT EXISTS previous_products_sub_category_gin_index ON previous_products USING gin(sub_category gin_trgm_ops);",
    "CREATE INDEX IF NOT EXISTS previous_products_title_gin_index ON previous_products USING gin(title gin_trgm_ops);",
    "CREATE INDEX IF NOT EXISTS ah_products_sub_category_gin_index ON ah_products USING gin(sub_category gin_trgm_ops);",
    "CREATE INDEX IF NOT EXISTS ah_products_title_gin_index ON ah_products USING gin(title gin_trgm_ops);",
]

with engine.connect() as connection:
    for statement in sql_setup_statements:
        connection.execute(text(statement))
    connection.commit()
