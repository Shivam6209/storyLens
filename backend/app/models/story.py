"""
Story database model
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from ..core.database import Base

class Story(Base):
    """Story model for storing generated stories"""
    
    __tablename__ = "stories"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    story_text = Column(Text, nullable=False)
    story_type = Column(String(20), nullable=False, default="story")  # "story" or "poem"
    image_filename = Column(String(255), nullable=False)
    audio_filename = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Story(id={self.id}, type={self.story_type}, created_at={self.created_at})>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "story_text": self.story_text,
            "story_type": self.story_type,
            "image_filename": self.image_filename,
            "audio_filename": self.audio_filename,
            "audio_url": f"/api/audio/{self.audio_filename}" if self.audio_filename else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        } 