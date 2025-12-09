from fastapi import APIRouter, HTTPException, Header
from app.utils.security import get_current_user, load_db, require_role

router = APIRouter(prefix="/admin", tags=["Admin"])


def check_admin(user):
    require_role("admin")(user)


@router.get("/users")
def get_users(authorization: str = Header(None)):
    user = get_current_user(authorization)
    check_admin(user)
    db = load_db()
    return {"users": db["users"]}


@router.get("/courses")
def get_courses(authorization: str = Header(None)):
    user = get_current_user(authorization)
    check_admin(user)
    db = load_db()
    return {"courses": db["courses"]}


@router.get("/purchases")
def get_purchases(authorization: str = Header(None)):
    user = get_current_user(authorization)
    check_admin(user)
    db = load_db()
    return {"purchases": db.get("purchases", [])}


@router.get("/payments")
def get_payments(authorization: str = Header(None)):
    user = get_current_user(authorization)
    check_admin(user)
    db = load_db()
    return {"payments": db.get("payments", [])}


@router.get("/live-requests")
def get_live_requests(authorization: str = Header(None)):
    user = get_current_user(authorization)
    check_admin(user)
    db = load_db()
    return {"live_class_requests": db.get("live_class_requests", [])}
