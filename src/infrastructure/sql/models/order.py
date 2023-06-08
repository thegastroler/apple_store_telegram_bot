from infrastructure.sql.db import Base
from sqlalchemy import (VARCHAR, BigInteger, Boolean, Column, DateTime,
                        ForeignKey)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression, func


class Order(Base):
    __tablename__ = "orders"
    order = Column(VARCHAR(90), primary_key=True, nullable=False, unique=True) 
    user_id = Column(BigInteger, ForeignKey("users.user_id", ondelete="SET NULL"), nullable=False)
    paid = Column(Boolean, default=expression.false(), nullable=False)
    name = Column(VARCHAR(90), nullable=True)
    phone_number = Column(VARCHAR(90), nullable=True)
    email = Column(VARCHAR(90), nullable=True)
    city = Column(VARCHAR(90), nullable=True)
    post_code = Column(VARCHAR(90), nullable=True)
    state = Column(VARCHAR(90), nullable=True)
    street_line1 = Column(VARCHAR(90), nullable=True)
    street_line2= Column(VARCHAR(90), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", backref="orders_user_id")

    class Config:
        orm_mode = True
