from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from backend.app.database import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255))
    filepath = Column(String(500))
    uploaded_at = Column(DateTime, default=datetime.utcnow)