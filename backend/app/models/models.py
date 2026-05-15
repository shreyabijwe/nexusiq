from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Supplier(Base):
    __tablename__ = "suppliers"
    supplier_id = Column(Integer, primary_key=True, index=True)
    supplier_name = Column(String(100))
    contact_email = Column(String(100))
    phone = Column(String(20))
    country = Column(String(50))
    city = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

class Product(Base):
    __tablename__ = "products"
    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(150))
    category = Column(String(50))
    unit_price = Column(Float)
    supplier_id = Column(Integer, ForeignKey("suppliers.supplier_id"))
    sku = Column(String(50), unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Customer(Base):
    __tablename__ = "customers"
    customer_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100))
    email = Column(String(100), unique=True)
    phone = Column(String(20))
    city = Column(String(50))
    country = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

class Order(Base):
    __tablename__ = "orders"
    order_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    order_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20))
    total_amount = Column(Float)
    shipping_address = Column(Text)
    delivery_date = Column(DateTime)

class OrderItem(Base):
    __tablename__ = "order_items"
    item_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"))
    product_id = Column(Integer, ForeignKey("products.product_id"))
    quantity = Column(Integer)
    unit_price = Column(Float)
    total_price = Column(Float)

class Inventory(Base):
    __tablename__ = "inventory"
    inventory_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.product_id"))
    quantity_in_stock = Column(Integer)
    reorder_level = Column(Integer)
    warehouse_location = Column(String(50))
    last_updated = Column(DateTime, default=datetime.utcnow)

class Logistics(Base):
    __tablename__ = "logistics"
    logistics_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"))
    carrier = Column(String(50))
    tracking_number = Column(String(100))
    dispatch_date = Column(DateTime)
    estimated_delivery = Column(DateTime)
    actual_delivery = Column(DateTime)
    status = Column(String(30))