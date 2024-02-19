from sqlalchemy import create_engine, Column, String, DateTime, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL = 'postgresql://secUREusER:StrongEnoughPassword)@51.250.26.59:5432/query'

engine = create_engine(URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Ticket(Base):
    __tablename__ = 'port'

    id = Column(Integer, primary_key=True, index=True)
    passenger_name = Column(String, nullable=False)
    passport = Column(String, nullable=False)
    id_ship = Column(Integer, nullable=False)
    direction = Column(String, nullable=False)

