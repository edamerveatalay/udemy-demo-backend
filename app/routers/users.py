from fastapi import APIRouter, HTTPException, Header, Depends
from app.utils.security import get_current_user, load_db
from typing import List

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
def me(authorization: str = Header(None)):
    """
    Mevcut kullanıcı bilgilerini döner (password hariç).
    """
    user = get_current_user(authorization)
    safe_user = {k: v for k, v in user.items() if k != "password"}
    return safe_user


@router.get("/me/courses")
def my_courses(authorization: str = Header(None)):
    """
    Kullanıcının satın aldığı kursları döner (full course objeleri).
    """
    user = get_current_user(authorization)
    db = load_db()
    purchased = user.get("purchased_courses", [])
    courses = [c for c in db.get("courses", []) if c["id"] in purchased]
    return courses
