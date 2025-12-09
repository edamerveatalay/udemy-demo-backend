from pydantic import BaseModel
from typing import List, Optional


class User(BaseModel):
    id: int
    name: str
    email: str
    role: str
    purchased_courses: Optional[List[int]] = []


class Course(BaseModel):
    id: int
    title: str
    description: str
    instructor_id: int
    price: float


class Purchase(BaseModel):
    user_id: int
    course_id: int
    status: str


class Payment(BaseModel):
    payment_id: str
    user_id: int
    course_id: int
    status: str


class LiveRequest(BaseModel):
    user_id: int
    instructor_id: int
    topic: Optional[str] = None
    status: str
