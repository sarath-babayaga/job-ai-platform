from pydantic import BaseModel
from datetime import datetime


class JobCreate(BaseModel):
    title: str
    company: str
    location: str
    description: str


class JobResponse(JobCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
