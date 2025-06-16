"""
API routes for StoryLens
"""
import os
import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..models.story import Story
from ..services.story_generator import StoryGeneratorService
from ..services.audio_service import AudioService
from ..core.config import settings

router = APIRouter()

# Initialize services
story_service = StoryGeneratorService()
audio_service = AudioService()

@router.post("/upload")
async def upload_and_generate_story(
    file: UploadFile = File(...),
    story_type: str = Form("story"),
    db: Session = Depends(get_db)
):
    """Upload an image and generate a story with audio narration"""
    
    # Validate file
    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Check file extension
    file_extension = file.filename.split('.')[-1].lower() if file.filename else ''
    if file_extension not in settings.allowed_extensions_list:
        raise HTTPException(
            status_code=400, 
            detail=f"File extension not allowed. Allowed: {', '.join(settings.allowed_extensions_list)}"
        )
    
    # Check file size
    file_content = await file.read()
    if len(file_content) > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400, 
            detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE / 1024 / 1024:.1f}MB"
        )
    
    try:
        # Generate story
        story_text = await story_service.generate_story(file_content, story_type)
        
        # Create story record
        story_id = str(uuid.uuid4())
        image_filename = f"{story_id}_{file.filename}"
        
        # Save image file
        image_path = os.path.join(settings.AUDIO_OUTPUT_DIR, image_filename)
        os.makedirs(settings.AUDIO_OUTPUT_DIR, exist_ok=True)
        with open(image_path, "wb") as f:
            f.write(file_content)
        
        # Generate audio
        audio_filename = await audio_service.generate_audio(story_text, story_id)
        
        # Save to database
        db_story = Story(
            id=story_id,
            story_text=story_text,
            story_type=story_type,
            image_filename=image_filename,
            audio_filename=audio_filename
        )
        db.add(db_story)
        db.commit()
        db.refresh(db_story)
        
        return db_story.to_dict()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@router.get("/stories")
async def get_stories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all stories with pagination"""
    stories = db.query(Story).offset(skip).limit(limit).all()
    return [story.to_dict() for story in stories]

@router.get("/stories/{story_id}")
async def get_story(story_id: str, db: Session = Depends(get_db)):
    """Get a specific story by ID"""
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return story.to_dict()

@router.delete("/stories/{story_id}")
async def delete_story(story_id: str, db: Session = Depends(get_db)):
    """Delete a story and its associated files"""
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    
    # Delete associated files
    if story.audio_filename:
        audio_service.delete_audio_file(story.audio_filename)
    
    if story.image_filename:
        image_path = os.path.join(settings.AUDIO_OUTPUT_DIR, story.image_filename)
        if os.path.exists(image_path):
            os.remove(image_path)
    
    # Delete from database
    db.delete(story)
    db.commit()
    
    return {"message": "Story deleted successfully"}

@router.get("/audio/{filename}")
async def get_audio_file(filename: str):
    """Stream audio file"""
    file_path = os.path.join(settings.AUDIO_OUTPUT_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    return FileResponse(
        file_path,
        media_type="audio/wav",
        filename=filename
    )

@router.get("/images/{filename}")
async def get_image_file(filename: str):
    """Get uploaded image file"""
    file_path = os.path.join(settings.AUDIO_OUTPUT_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image file not found")
    
    return FileResponse(file_path) 