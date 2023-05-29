from datetime import datetime

from infrastructure.sql.db import Base
from sqlalchemy import VARCHAR, BigInteger, Boolean, Column, DateTime
from sqlalchemy.sql import expression


class User(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False)
    username = Column(VARCHAR(90), nullable=False)
    is_admin = Column(Boolean, default=expression.false(), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    class Config:
        orm_mode = True
