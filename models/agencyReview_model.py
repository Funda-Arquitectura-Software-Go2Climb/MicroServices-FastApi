from pydantic import BaseModel
from typing import Optional
from datetime import date

class AgencyReview_model(BaseModel):
    id: Optional[str]
    date: str
    comment: str
    professionalism_score: str
    security_score: str
    quality_score: str
    cost_score: str
    agency: Optional[str]
    tourist: Optional[str]
