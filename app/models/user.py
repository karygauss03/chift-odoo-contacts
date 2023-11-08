from sqlalchemy import Integer, String, Column
from ..database import Base

class User(Base):
    __tablename__='users'
    id=Column(Integer, primary_key=True, nullable=False)
    email=Column(String, unique=True, nullable=False)
    password=Column(String, nullable=False)
