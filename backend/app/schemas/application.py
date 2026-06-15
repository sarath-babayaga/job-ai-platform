from pydantic import BaseModel
from datetime import datetime


class ApplicationCreate(BaseModel):
    resume_id: int
    job_id: int


class ApplicationResponse(BaseModel):
    id: int
    resume_id: int
    job_id: int
    status: str
    applied_at: datetime

    class Config:
        from_attributes = True