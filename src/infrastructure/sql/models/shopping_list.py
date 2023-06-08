from infrastructure.sql.db import Base
from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class ShoppingList(Base):
    __tablename__ = "shopping_list"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.user_id", ondelete="SET NULL"), nullable=False)
    item_id = Column(BigInteger, ForeignKey("items.id", ondelete="SET NULL"), nullable=False)
    order_id = Column(VARCHAR(90), ForeignKey("orders.order", ondelete="SET NULL"), nullable=False) 
    quantity = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", backref="shopping_list_user_id")
    item = relationship("Item", backref="item_id")
    order = relationship("Order", backref="order_order")

    class Config:
        orm_mode = True
