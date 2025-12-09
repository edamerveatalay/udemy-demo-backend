from pydantic import BaseModel


class Purchase(BaseModel):
    user_id: int
    course_id: int
    status: str  # "success" | "failed"
