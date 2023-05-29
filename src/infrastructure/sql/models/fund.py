from datetime import datetime

from infrastructure.sql.db import Base
from sqlalchemy import (VARCHAR, Boolean, Column, DateTime, BigInteger,
                        SmallInteger, UniqueConstraint, ForeignKey)
from sqlalchemy.orm import relationship, backref


class Fund(Base):
    __tablename__ = "fund"
    id = Column(BigInteger, primary_key=True, autoincrement=True)

    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    item_id = Column(BigInteger, ForeignKey("items.id", ondelete="SET NULL"), nullable=True)

    bought = Column(Boolean, default=False)
    label = Column(VARCHAR(50), default=1)

    user = relationship("User", backref=backref("users"))
    item = relationship("Item", backref=backref("items"))

    class Config:
        orm_mode = True
