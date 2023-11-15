from pydantic import BaseModel
from typing import Optional
from datetime import date

class Tourist(BaseModel):
    id: Optional[int]
    name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    phone_number: Optional[str]
    photo: Optional[str]

    class Config:
        orm_mode = True
