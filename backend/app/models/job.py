from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

from backend.app.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255))
    company = Column(String(255))
    location = Column(String(255))

    description = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)