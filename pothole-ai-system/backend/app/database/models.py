"""Report model for SQLite."""
from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.sql import func

from database.db import Base


class ReportModel(Base):
    __tablename__ = "reports"

    id = Column(String, primary_key=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    issue_type = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    status = Column(String, nullable=False, default="open")
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    image_path = Column(String, nullable=True)
