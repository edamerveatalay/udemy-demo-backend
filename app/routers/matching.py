from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
import json

from app.utils.security import get_current_user, load_db

router = APIRouter(prefix="/live", tags=["Live Class Matching"])


class LiveClassRequest(BaseModel):
    topic: str


def save_db(data):
    with open("app/mock/db.json", "w") as f:
        json.dump(data, f, indent=2)


@router.post("/request")
def request_live_class(body: LiveClassRequest, authorization: str = Header(None)):
    user = get_current_user(authorization)

    if user["role"] != "user":
        raise HTTPException(
            status_code=403, detail="Sadece öğrenciler canlı ders talebi oluşturabilir"
        )

    db = load_db()

    instructors = [u for u in db["users"] if u["role"] == "instructor"]

    if not instructors:
        raise HTTPException(status_code=404, detail="Sistemde uygun eğitmen yok!")

    assigned_instructor = instructors[0]

    request_record = {
        "user_id": user["id"],
        "instructor_id": assigned_instructor["id"],
        "topic": body.topic,
        "status": "assigned",
    }

    db["live_class_requests"].append(request_record)
    save_db(db)

    return {
        "message": "Canlı ders talebi oluşturuldu",
        "assigned_instructor": assigned_instructor["name"],
        "instructor_id": assigned_instructor["id"],
        "notification": f"Eğitmen {assigned_instructor['name']} için bildirim gönderildi (simülasyon)",
    }
