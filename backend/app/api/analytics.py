from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.models import Order, OrderItem, Product
import numpy as np
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/demand-forecast")
def demand_forecast(db: Session = Depends(get_db)):
    result = db.query(
        func.date_trunc('month', Order.order_date).label('month'),
        func.sum(Order.total_amount).label('revenue')
    ).group_by('month').order_by('month').all()

    if len(result) < 3:
        return {"error": "Not enough data"}

    revenues = [float(r[1]) for r in result]
    x = np.arange(len(revenues))

    coeffs = np.polyfit(x, revenues, 1)
    slope, intercept = coeffs

    forecast = []
    last_date = result[-1][0]
    for i in range(1, 4):
        next_month = last_date + timedelta(days=32 * i)
        next_month = next_month.replace(day=1)
        predicted = slope * (len(revenues) + i - 1) + intercept
        forecast.append({
            "month": next_month.strftime("%Y-%m"),
            "predicted_revenue": round(max(predicted, 0), 2),
            "type": "forecast"
        })

    historical = [{"month": str(r[0])[:7], "revenue": round(float(r[1]), 2), "type": "actual"} for r in result[-6:]]

    return {"historical": historical, "forecast": forecast}

@router.get("/anomaly-detection")
def detect_anomalies(db: Session = Depends(get_db)):
    result = db.query(
        func.date_trunc('day', Order.order_date).label('day'),
        func.sum(Order.total_amount).label('revenue'),
        func.count(Order.order_id).label('order_count')
    ).group_by('day').order_by('day').all()

    if len(result) < 7:
        return {"anomalies": [], "normal_days": []}

    revenues = [float(r[1]) for r in result]
    mean = np.mean(revenues)
    std = np.std(revenues)

    anomalies = []
    normal = []

    for r in result[-30:]:
        revenue = float(r[1])
        z_score = (revenue - mean) / std if std > 0 else 0
        point = {
            "day": str(r[0])[:10],
            "revenue": round(revenue, 2),
            "order_count": int(r[2]),
            "z_score": round(z_score, 2)
        }
        if abs(z_score) > 2:
            anomalies.append(point)
        else:
            normal.append(point)

    return {"anomalies": anomalies, "normal_days": normal[-10:]}

@router.get("/executive-summary")
def executive_summary(db: Session = Depends(get_db)):
    from app.models.models import Inventory, Logistics

    total_revenue = db.query(func.sum(Order.total_amount)).scalar() or 0
    total_orders = db.query(func.count(Order.order_id)).scalar() or 0
    avg_order = total_revenue / total_orders if total_orders > 0 else 0
    low_stock = db.query(func.count(Inventory.inventory_id))\
        .filter(Inventory.quantity_in_stock <= Inventory.reorder_level).scalar()
    delivered = db.query(func.count(Logistics.logistics_id))\
        .filter(Logistics.status == 'delivered').scalar()
    total_shipments = db.query(func.count(Logistics.logistics_id)).scalar()
    delivery_rate = (delivered / total_shipments * 100) if total_shipments > 0 else 0

    summary = f"""
    NexusIQ Executive Summary — {datetime.now().strftime('%B %Y')}

    REVENUE: Total platform revenue stands at ${total_revenue:,.2f} across {total_orders:,} orders,
    with an average order value of ${avg_order:,.2f}.

    INVENTORY: {low_stock} products are currently at or below reorder levels and require
    immediate attention to avoid stockouts.

    LOGISTICS: The platform has processed {total_shipments:,} shipments with a delivery
    success rate of {delivery_rate:.1f}%.

    RECOMMENDATION: {'Reorder low stock items immediately.' if low_stock > 5 else 'Inventory levels are healthy.'}
    {'Investigate delivery failures.' if delivery_rate < 80 else 'Logistics performance is strong.'}
    """

    return {"summary": summary.strip(), "metrics": {
        "total_revenue": round(total_revenue, 2),
        "total_orders": total_orders,
        "avg_order_value": round(avg_order, 2),
        "low_stock_items": low_stock,
        "delivery_rate": round(delivery_rate, 1)
    }}