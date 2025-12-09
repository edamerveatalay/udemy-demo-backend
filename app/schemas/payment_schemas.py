from pydantic import BaseModel


class PaymentCreateRequestSchema(BaseModel):
    course_id: int


class PaymentConfirmRequestSchema(BaseModel):
    payment_id: str


class PaymentCreateResponseSchema(BaseModel):
    payment_id: str
    status: str
    redirect_url: str
    note: str


class PaymentConfirmResponseSchema(BaseModel):
    status: str
