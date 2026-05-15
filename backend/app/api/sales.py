from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.models import Order, Customer, Product

router = APIRouter()

@router.get("/summary")
def get_sales_summary(db: Session = Depends(get_db)):
    total_revenue = db.query(func.sum(Order.total_amount)).scalar() or 0
    total_orders = db.query(func.count(Order.order_id)).scalar() or 0
    total_customers = db.query(func.count(Customer.customer_id)).scalar() or 0
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

    return {
        "total_revenue": round(total_revenue, 2),
        "total_orders": total_orders,
        "total_customers": total_customers,
        "avg_order_value": round(avg_order_value, 2)
    }

@router.get("/by-status")
def get_orders_by_status(db: Session = Depends(get_db)):
    result = db.query(Order.status, func.count(Order.order_id))\
        .group_by(Order.status).all()
    return [{"status": r[0], "count": r[1]} for r in result]

@router.get("/monthly-revenue")
def get_monthly_revenue(db: Session = Depends(get_db)):
    result = db.query(
        func.date_trunc('month', Order.order_date).label('month'),
        func.sum(Order.total_amount).label('revenue')
    ).group_by('month').order_by('month').all()
    return [{"month": str(r[0]), "revenue": round(r[1], 2)} for r in result]

@router.get("/top-products")
def get_top_products(db: Session = Depends(get_db)):
    from app.models.models import OrderItem
    result = db.query(
        Product.product_name,
        func.sum(OrderItem.total_price).label('revenue')
    ).join(OrderItem, Product.product_id == OrderItem.product_id)\
     .group_by(Product.product_name)\
     .order_by(func.sum(OrderItem.total_price).desc())\
     .limit(10).all()
    return [{"product": r[0], "revenue": round(r[1], 2)} for r in result]