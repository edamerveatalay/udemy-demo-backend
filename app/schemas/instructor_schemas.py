from pydantic import BaseModel
from typing import List, Optional


class Notification(BaseModel):
    message: str
    timestamp: Optional[str] = None


class NotificationsResponse(BaseModel):
    notifications: List[Notification]


class ClearNotificationsResponse(BaseModel):
    message: str
