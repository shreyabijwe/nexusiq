from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import sales, inventory, logistics, auth, analytics

app = FastAPI(
    title="NexusIQ API",
    description="Retail & Supply Chain Decision Intelligence Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(sales.router, prefix="/api/sales", tags=["Sales"])
app.include_router(inventory.router, prefix="/api/inventory", tags=["Inventory"])
app.include_router(logistics.router, prefix="/api/logistics", tags=["Logistics"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])

@app.get("/")
def root():
    return {"message": "NexusIQ API is running", "version": "1.0.0"}