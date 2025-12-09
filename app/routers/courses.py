from fastapi import APIRouter, HTTPException
from app.utils.security import load_db

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.get("/")
def get_all_courses():
    db = load_db()
    return db["courses"]


@router.get("/{course_id}")
def get_course(course_id: int):
    db = load_db()

    for course in db["courses"]:
        if course["id"] == course_id:
            return course

    raise HTTPException(status_code=404, detail="Kurs bulunamadı")
