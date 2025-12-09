from fastapi import APIRouter, HTTPException, Header
from typing import List
import json

from app.utils.security import get_current_user, load_db
from app.schemas.users_schemas import UserMeResponseSchema, CourseSchema

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserMeResponseSchema)
def me(authorization: str = Header(None)):
    """
    Mevcut kullanıcı bilgilerini döner (password hariç).
    """
    user = get_current_user(authorization)
    safe_user = {k: v for k, v in user.items() if k != "password"}
    return safe_user


@router.get("/me/courses", response_model=List[CourseSchema])
def my_courses(authorization: str = Header(None)):
    """
    Kullanıcının satın aldığı kursları döner (full course objeleri).
    """
    user = get_current_user(authorization)
    db = load_db()
    purchased = user.get("purchased_courses", [])
    courses = [c for c in db.get("courses", []) if c["id"] in purchased]
    return courses
