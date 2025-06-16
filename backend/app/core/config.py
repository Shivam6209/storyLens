"""
Configuration settings for StoryLens backend
"""
import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    API_BASE_URL: str = "http://localhost:8000"
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    # Hugging Face API
    HUGGINGFACE_API_KEY: str = ""
    
    # Database Configuration
    DB_HOST: str = ""
    DB_PORT: int = 5432
    DB_USERNAME: str = ""
    DB_PASSWORD: str = ""
    DB_DATABASE: str = ""
    DATABASE_URL: str = ""
    
    # Audio Settings
    AUDIO_OUTPUT_DIR: str = "./audio_files"
    MAX_AUDIO_DURATION: int = 300
    
    # File Upload Settings
    MAX_FILE_SIZE: int = 10485760  # 10MB
    ALLOWED_EXTENSIONS: List[str] = ["jpg", "jpeg", "png", "webp"]
    
    # Development Settings
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    # Model Settings
    KOSMOS_MODEL_ID: str = "microsoft/kosmos-2-patch14-224"
    TTS_MODEL_NAME: str = "tts_models/multilingual/multi-dataset/xtts_v2"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Parse CORS_ORIGINS if it's a string
        if isinstance(self.CORS_ORIGINS, str):
            self.CORS_ORIGINS = [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
        
        # Build DATABASE_URL if not provided and individual components are available
        if not self.DATABASE_URL and all([self.DB_HOST, self.DB_USERNAME, self.DB_PASSWORD, self.DB_DATABASE]):
            self.DATABASE_URL = f"postgresql://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_DATABASE}"

# Create settings instance
settings = Settings() 