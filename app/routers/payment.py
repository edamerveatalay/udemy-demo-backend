from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
import json
import uuid
import threading
import time

from app.utils.security import get_current_user, load_db

router = APIRouter(prefix="/payment", tags=["Payment"])


def save_db(data):
    with open("app/mock/db.json", "w") as f:
        json.dump(data, f, indent=2)


class PaymentCreateRequest(BaseModel):
    course_id: int


class PaymentConfirmRequest(BaseModel):
    payment_id: str


def auto_confirm(payment_id: str):
    time.sleep(1)

    db = load_db()
    payment = next(
        (p for p in db.get("payments", []) if p["payment_id"] == payment_id), None
    )
    if not payment:
        return

    payment["status"] = "success"

    for u in db["users"]:
        if u["id"] == payment["user_id"]:
            if "purchased_courses" not in u:
                u["purchased_courses"] = []
            if payment["course_id"] not in u["purchased_courses"]:
                u["purchased_courses"].append(payment["course_id"])

    save_db(db)


@router.post(
    "/create",
    summary="Create Payment (Demo)",
    description=(
        "Kullanıcı için ödeme kaydı oluşturur.\n\n"
        "Demo ortamında ödeme kısa bir süre içinde otomatik olarak confirm edilir ve kurs kullanıcıya atanır.\n"
        "Manuel confirm için /payment/confirm endpoint'i kullanılabilir."
    ),
)
def create_payment(body: PaymentCreateRequest, authorization: str = Header(None)):
    user = get_current_user(authorization)
    db = load_db()

    course_exists = any(c["id"] == body.course_id for c in db["courses"])
    if not course_exists:
        raise HTTPException(status_code=404, detail="Kurs bulunamadı")

    payment_id = str(uuid.uuid4())

    if "payments" not in db:
        db["payments"] = []

    db["payments"].append(
        {
            "payment_id": payment_id,
            "user_id": user["id"],
            "course_id": body.course_id,
            "status": "pending",
        }
    )
    save_db(db)

    threading.Thread(target=auto_confirm, args=(payment_id,), daemon=True).start()

    return {
        "payment_id": payment_id,
        "status": "pending",
        "redirect_url": f"/payment/simulate/{payment_id}",
        "note": "Ödeme kısa süre içinde otomatik olarak tamamlanacaktır",
    }


@router.post(
    "/confirm",
    summary="Confirm Payment (Manual, optional)",
    description=(
        "Ödemeyi manuel olarak confirm etmek için kullanılır.\n"
        "Normal kullanıcı akışında /payment/create ile başlatılan ödeme, "
        "arka planda otomatik olarak confirm edilir.\n"
        "Bu endpoint test veya özel senaryolar için opsiyoneldir."
    ),
)
def confirm_payment(body: PaymentConfirmRequest):
    db = load_db()
    payment = next(
        (p for p in db.get("payments", []) if p["payment_id"] == body.payment_id), None
    )
    if not payment:
        raise HTTPException(status_code=404, detail="Payment bulunamadı")

    payment["status"] = "success"

    for u in db["users"]:
        if u["id"] == payment["user_id"]:
            if "purchased_courses" not in u:
                u["purchased_courses"] = []
            if payment["course_id"] not in u["purchased_courses"]:
                u["purchased_courses"].append(payment["course_id"])

    save_db(db)
    return {"status": "success"}
