from pydantic import BaseModel
from typing import List, Optional


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: str
    purchased_courses: Optional[List[int]] = []


class CourseOut(BaseModel):
    id: int
    title: str
    description: str
    instructor_id: int
    price: float


class PurchaseOut(BaseModel):
    user_id: int
    course_id: int
    status: str


class PaymentOut(BaseModel):
    payment_id: str
    user_id: int
    course_id: int
    status: str


class LiveRequestOut(BaseModel):
    user_id: int
    instructor_id: int
    topic: Optional[str] = None
    status: str
