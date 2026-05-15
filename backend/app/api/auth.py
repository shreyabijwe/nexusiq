from fastapi import APIRouter, HTTPException
from app.schemas.schemas import UserLogin, Token
from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "nexusiq-secret-key-2024"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

FAKE_USER = {
    "username": "admin",
    "password": "admin123"
}

router = APIRouter()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/login", response_model=Token)
def login(user: UserLogin):
    if user.username != FAKE_USER["username"] or user.password != FAKE_USER["password"]:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}