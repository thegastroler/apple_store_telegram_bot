from datetime import datetime

from infrastructure.sql.db import Base
from sqlalchemy import BigInteger, Boolean, Column, DateTime, ForeignKey, Text, Integer
from sqlalchemy.orm import relationship, aliased
from sqlalchemy.sql import expression


class ShoppingCart(Base):
    __tablename__ = "shopping_cart"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.user_id", ondelete="SET NULL"), nullable=False)
    item_id = Column(BigInteger, ForeignKey("items.id", ondelete="SET NULL"), nullable=False)
    order_id = Column(Text, nullable=False) 
    paid = Column(Boolean, default=expression.false(), nullable=False)
    quantity = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="shopping_cart_user_id")
    item = relationship("Item", backref="item_id")

    class Config:
        orm_mode = True
