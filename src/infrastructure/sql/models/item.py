from datetime import datetime

from infrastructure.sql.db import Base
from sqlalchemy import (VARCHAR, BigInteger, Column, DateTime, ForeignKey,
                        Integer)
from sqlalchemy.orm import backref, relationship


class Item(Base):
    __tablename__ = "items"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(255), nullable=False)
    article = Column(VARCHAR(90), nullable=True)

    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)

    price = Column(Integer, nullable=False, default=0)
    total = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    category = relationship("Category", backref=backref("categories"))

    class Config:
        orm_mode = True
