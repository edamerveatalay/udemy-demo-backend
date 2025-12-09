from pydantic import BaseModel


class LiveClassRequestSchema(BaseModel):
    topic: str


class LiveClassResponseSchema(BaseModel):
    message: str
    assigned_instructor: str
    instructor_id: int
    notification: str
