from infrastructure.sql.db import Base
from sqlalchemy import VARCHAR, BigInteger, Boolean, Column, DateTime
from sqlalchemy.sql import expression, func


class User(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, primary_key=True, unique=True)
    username = Column(VARCHAR(90), nullable=False)
    banned = Column(Boolean, default=False, nullable=True)
    is_admin = Column(Boolean, default=expression.false(), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    class Config:
        orm_mode = True
