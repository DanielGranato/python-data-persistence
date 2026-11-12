import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()  # carrega o .env
DATABASE_URL = os.getenv("DATABASE_URL")  # pega o valor

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL não definida. Crie o arquivo .env em fastapi-postgres/ "
        "a partir do .env.example."
    )

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

