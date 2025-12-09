from pydantic import BaseModel
from typing import List, Optional, Dict


class UserBaseSchema(BaseModel):
    id: int
    name: str
    email: str
    role: str


class UserMeResponseSchema(UserBaseSchema):
    purchased_courses: Optional[List[int]] = []


class CourseSchema(BaseModel):
    id: int
    title: str
    description: str
    instructor: str
    price: float
