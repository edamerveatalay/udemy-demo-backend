from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json

from app.utils.security import create_fake_token, load_db

router = APIRouter(prefix="/auth", tags=["Auth"])


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/login")
def login(data: LoginRequest):
    db = load_db()

    for user in db["users"]:
        if user["email"] == data.email and user["password"] == data.password:
            token = create_fake_token(user["id"])
            return {
                "message": "Login successful",
                "token": token,
                "role": user["role"],
                "user_id": user["id"],
            }

    raise HTTPException(status_code=401, detail="Email veya şifre yanlış")
