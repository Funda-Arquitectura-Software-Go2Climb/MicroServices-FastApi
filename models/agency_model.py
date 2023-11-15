from pydantic import BaseModel
from typing import Optional

class Agency(BaseModel):
    id: Optional[int]
    name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    phoneNumber: Optional[str]
    description: Optional[str]
    location: Optional[str]
    ruc: Optional[str]
    photo: Optional[str]
    score: Optional[str]

    class Config:
        orm_mode = True
