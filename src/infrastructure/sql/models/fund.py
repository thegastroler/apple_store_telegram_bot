from infrastructure.sql.db import Base
from sqlalchemy import (VARCHAR, BigInteger, Boolean, Column, ForeignKey,
                        Integer)
from sqlalchemy.orm import backref, relationship


class Fund(Base):
    __tablename__ = "fund"
    id = Column(BigInteger, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    item_id = Column(Integer, ForeignKey("items.id", ondelete="SET NULL"), nullable=True)

    bought = Column(Boolean, default=False)
    label = Column(VARCHAR(50), default=1)

    user = relationship("User", backref=backref("users"))
    item = relationship("Item", backref=backref("items"))

    class Config:
        orm_mode = True
