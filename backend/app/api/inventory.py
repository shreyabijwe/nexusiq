from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.models import Inventory, Product

router = APIRouter()

@router.get("/summary")
def get_inventory_summary(db: Session = Depends(get_db)):
    total_products = db.query(func.count(Inventory.inventory_id)).scalar()
    low_stock = db.query(func.count(Inventory.inventory_id))\
        .filter(Inventory.quantity_in_stock <= Inventory.reorder_level).scalar()
    out_of_stock = db.query(func.count(Inventory.inventory_id))\
        .filter(Inventory.quantity_in_stock == 0).scalar()
    return {
        "total_products": total_products,
        "low_stock_items": low_stock,
        "out_of_stock_items": out_of_stock
    }

@router.get("/all")
def get_all_inventory(db: Session = Depends(get_db)):
    result = db.query(Inventory, Product)\
        .join(Product, Inventory.product_id == Product.product_id)\
        .limit(100).all()
    return [{
        "inventory_id": r[0].inventory_id,
        "product_name": r[1].product_name,
        "category": r[1].category,
        "quantity_in_stock": r[0].quantity_in_stock,
        "reorder_level": r[0].reorder_level,
        "warehouse_location": r[0].warehouse_location,
        "status": "Low Stock" if r[0].quantity_in_stock <= r[0].reorder_level else "OK"
    } for r in result]

@router.get("/by-warehouse")
def get_inventory_by_warehouse(db: Session = Depends(get_db)):
    result = db.query(
        Inventory.warehouse_location,
        func.sum(Inventory.quantity_in_stock).label('total_stock')
    ).group_by(Inventory.warehouse_location).all()
    return [{"warehouse": r[0], "total_stock": r[1]} for r in result]