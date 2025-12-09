from pydantic import BaseModel


class LiveClassRequest(BaseModel):
    user_id: int
    instructor_id: int
    status: str
