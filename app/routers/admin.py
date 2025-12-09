from fastapi import APIRouter, HTTPException, Header
from typing import List
from app.utils.security import get_current_user, load_db, require_role
from app.schemas.admin_schemas import (
    UserOut,
    CourseOut,
    PurchaseOut,
    PaymentOut,
    LiveRequestOut,
)

router = APIRouter(prefix="/admin", tags=["Admin"])


def check_admin(user):
    require_role("admin")(user)


@router.get("/users", response_model=List[UserOut])
def get_users(authorization: str = Header(None)):
    user = get_current_user(authorization)
    check_admin(user)
    db = load_db()
    return db["users"]


@router.get("/courses", response_model=List[CourseOut])
def get_courses(authorization: str = Header(None)):
    user = get_current_user(authorization)
    check_admin(user)
    db = load_db()
    return db["courses"]


@router.get("/purchases", response_model=List[PurchaseOut])
def get_purchases(authorization: str = Header(None)):
    user = get_current_user(authorization)
    check_admin(user)
    db = load_db()
    return db.get("purchases", [])


@router.get("/payments", response_model=List[PaymentOut])
def get_payments(authorization: str = Header(None)):
    user = get_current_user(authorization)
    check_admin(user)
    db = load_db()
    return db.get("payments", [])


@router.get("/live-requests", response_model=List[LiveRequestOut])
def get_live_requests(authorization: str = Header(None)):
    user = get_current_user(authorization)
    check_admin(user)
    db = load_db()
    return db.get("live_class_requests", [])
