from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class VisitBase(BaseModel):
    visitor_email: str
    visitor_oauth_token: str
    visited_user_email: str

class VisitCreate(VisitBase):
    pass

class VisitResponse(VisitBase):
    id: str
    timestamp: datetime
