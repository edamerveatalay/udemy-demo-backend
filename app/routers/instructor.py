from fastapi import APIRouter, HTTPException, Header
from app.utils.security import get_current_user, load_db
from app.schemas.instructor_schemas import (
    NotificationsResponse,
    ClearNotificationsResponse,
)
import json

router = APIRouter(prefix="/instructor", tags=["Instructor"])


def save_db(data):
    with open("app/mock/db.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


@router.get("/notifications", response_model=NotificationsResponse)
def notifications(authorization: str = Header(None)):
    """
    Eğitmenin bildirim listesini döner.
    """
    user = get_current_user(authorization)
    if user.get("role") != "instructor":
        raise HTTPException(status_code=403, detail="Sadece eğitmenler erişebilir")
    db = load_db()
    instr = next((u for u in db["users"] if u["id"] == user["id"]), None)
    if not instr:
        raise HTTPException(status_code=404, detail="Eğitmen bulunamadı")
    return {"notifications": instr.get("notifications", [])}


@router.post("/notifications/clear", response_model=ClearNotificationsResponse)
def clear_notifications(authorization: str = Header(None)):
    """
    Eğitmenin bildirimlerini temizler.
    """
    user = get_current_user(authorization)
    if user.get("role") != "instructor":
        raise HTTPException(status_code=403, detail="Sadece eğitmenler erişebilir")
    db = load_db()
    for u in db["users"]:
        if u["id"] == user["id"]:
            u["notifications"] = []
            break
    save_db(db)
    return {"message": "Notifications cleared"}
