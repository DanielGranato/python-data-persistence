import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import sessionmaker

load_dotenv()  # carrega o .env
DATABASE_URL = os.getenv("DATABASE_URL")  # pega o valor

