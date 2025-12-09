from fastapi import APIRouter, HTTPException
from app.utils.security import load_db
from app.schemas.courses_schemas import Course

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.get("/", response_model=list[Course])
def get_all_courses():
    db = load_db()
    return db["courses"]


@router.get("/{course_id}", response_model=Course)
def get_course(course_id: int):
    db = load_db()

    for course in db["courses"]:
        if course["id"] == course_id:
            return course

    raise HTTPException(status_code=404, detail="Kurs bulunamadı")
