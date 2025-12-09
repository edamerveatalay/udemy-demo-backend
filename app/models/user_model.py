from pydantic import BaseModel
from typing import Optional, List


class User(BaseModel):
    id: int
    name: str
    email: str
    password: str
    role: str
    purchased_courses: Optional[List[int]] = []
