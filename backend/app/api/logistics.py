from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.models import Logistics

router = APIRouter()

@router.get("/summary")
def get_logistics_summary(db: Session = Depends(get_db)):
    total = db.query(func.count(Logistics.logistics_id)).scalar()
    delivered = db.query(func.count(Logistics.logistics_id))\
        .filter(Logistics.status == "delivered").scalar()
    pending = db.query(func.count(Logistics.logistics_id))\
        .filter(Logistics.status == "pending").scalar()
    shipped = db.query(func.count(Logistics.logistics_id))\
        .filter(Logistics.status == "shipped").scalar()
    return {
        "total_shipments": total,
        "delivered": delivered,
        "pending": pending,
        "shipped": shipped
    }

@router.get("/by-carrier")
def get_by_carrier(db: Session = Depends(get_db)):
    result = db.query(
        Logistics.carrier,
        func.count(Logistics.logistics_id).label('shipments')
    ).group_by(Logistics.carrier).all()
    return [{"carrier": r[0], "shipments": r[1]} for r in result]

@router.get("/recent")
def get_recent_shipments(db: Session = Depends(get_db)):
    result = db.query(Logistics)\
        .order_by(Logistics.dispatch_date.desc())\
        .limit(20).all()
    return [{
        "logistics_id": r.logistics_id,
        "order_id": r.order_id,
        "carrier": r.carrier,
        "tracking_number": r.tracking_number,
        "status": r.status,
        "dispatch_date": str(r.dispatch_date),
        "estimated_delivery": str(r.estimated_delivery)
    } for r in result]