from sqlalchemy import create_engine, Table, Integer, String, Float, MetaData, Column
from sqlalchemy.orm import (
    declarative_base,
    Session,
    Mapped,
    mapped_column,
    DeclarativeBase,
)
from typing import Optional
from dotenv import load_dotenv
import os
from sqlalchemy.engine import URL

load_dotenv()

DB_DRIVER = os.getenv("DB_DRIVER")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_DATABASE = os.getenv("DB_DATABASE")

db_url = URL.create(
    drivername=DB_DRIVER,
    username=DB_USERNAME,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_DATABASE,
)

engine = create_engine(db_url, echo=True)

metadata = MetaData()


class Base(DeclarativeBase):
    pass


class Data(Base):
    __tablename__ = "data_storage"
    id: Mapped[Optional[int]] = mapped_column(primary_key=True)
    input: Mapped[str] = mapped_column(String(100), nullable=False)
    sentiment_output: Mapped[str] = mapped_column(String(20), nullable=False)
    confidence: Mapped[float] = mapped_column(nullable=False)


def input_data(**kwargs):
    with Session(engine) as session:
        new_record = Data(**kwargs)
        session.add(new_record)
        session.commit()


# input_data(input="Im sad", sentiment_output="Negative", confidence=99.87462)

# Base.metadata.create_all(engine) # first time creation
