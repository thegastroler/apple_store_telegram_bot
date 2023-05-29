from datetime import datetime

from infrastructure.sql.db import Base
from sqlalchemy import VARCHAR, BigInteger, Column, DateTime


class Category(Base):
    __tablename__ = "categories"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(90), nullable=False)

    class Config:
        orm_mode = True
