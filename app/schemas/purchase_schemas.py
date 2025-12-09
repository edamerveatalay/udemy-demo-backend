from pydantic import BaseModel


class PurchaseRequestSchema(BaseModel):
    course_id: int


class PurchaseResponseSchema(BaseModel):
    message: str
    course_id: int
