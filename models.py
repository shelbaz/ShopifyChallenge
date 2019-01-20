from sqlalchemy import Column, DateTime, ForeignKey, Integer, Float, String, func
from sqlalchemy.orm import backref, relationship

from database import Base

## DB model

class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    title = Column(String(30), nullable=False)
    price = Column(Float)
    quantity = Column(Integer)

class CartItem(Base):
    __tablename__ = 'cart_item'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    quantity = Column(Integer)
    price = Column(Float)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)


class ShoppingCart(Base):
    __tablename__ = 'cart'
    id = Column(Integer, primary_key=True)
    total_price = Column(Float)
    cart_item_id = Column(Integer, ForeignKey(CartItem.id))
    cart_item = relationship(CartItem, cascade="delete, delete-orphan", single_parent=True)


class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    total_price = Column(Float)
    cart_item_id = Column(Integer, ForeignKey(CartItem.id))
    cart_item = relationship(CartItem, cascade="delete, delete-orphan", single_parent=True)
