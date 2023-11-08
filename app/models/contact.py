from sqlalchemy import Integer, String, Column
from ..database import Base

class Contact(Base):
    __tablename__='contacts'
    id=Column(Integer, primary_key=True, nullable=False)
    name=Column(String, nullable=False)
    email=Column(String, unique=True, nullable=False)
