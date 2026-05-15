from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SalesSummary(BaseModel):
    total_revenue: float
    total_orders: int
    avg_order_value: float
    total_customers: int

class OrderOut(BaseModel):
    order_id: int
    customer_id: int
    order_date: datetime
    status: str
    total_amount: float

    class Config:
        from_attributes = True

class InventoryOut(BaseModel):
    inventory_id: int
    product_id: int
    quantity_in_stock: int
    reorder_level: int
    warehouse_location: str

    class Config:
        from_attributes = True

class LogisticsOut(BaseModel):
    logistics_id: int
    order_id: int
    carrier: str
    tracking_number: str
    status: str
    dispatch_date: Optional[datetime]
    estimated_delivery: Optional[datetime]

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str