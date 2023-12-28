from sqlalchemy import create_engine
from config import Config
from database.model import Base


config = Config()
engine = create_engine(
        f"postgresql://{config.get('database')['username']}:{config.get('database')['password']}@{config.get('database')['host']}/{config.get('database')['name']}"
    )
Base.metadata.create_all(engine)
