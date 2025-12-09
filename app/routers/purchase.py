from fastapi import APIRouter, HTTPException, Header
import json

from app.utils.security import get_current_user, load_db
from app.schemas.purchase_schemas import PurchaseRequestSchema, PurchaseResponseSchema

router = APIRouter(prefix="/purchase", tags=["Purchase"])


def save_db(data):
    with open("app/mock/db.json", "w") as f:
        json.dump(data, f, indent=2)


@router.post("/", response_model=PurchaseResponseSchema)
def purchase_course(body: PurchaseRequestSchema, authorization: str = Header(None)):
    user = get_current_user(authorization)
    db = load_db()

    if "purchased_courses" in user and body.course_id in user["purchased_courses"]:
        raise HTTPException(status_code=400, detail="Bu kurs zaten satın alınmış")

    course_exists = any(c["id"] == body.course_id for c in db["courses"])
    if not course_exists:
        raise HTTPException(status_code=404, detail="Kurs bulunamadı")

    payment_status = "success"

    for u in db["users"]:
        if u["id"] == user["id"]:
            if "purchased_courses" not in u:
                u["purchased_courses"] = []
            u["purchased_courses"].append(body.course_id)

    if "purchases" not in db:
        db["purchases"] = []

    db["purchases"].append(
        {"user_id": user["id"], "course_id": body.course_id, "status": payment_status}
    )

    save_db(db)

    return {"message": "Satın alma başarılı", "course_id": body.course_id}
