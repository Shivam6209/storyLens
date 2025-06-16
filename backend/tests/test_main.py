"""
Tests for the main FastAPI application
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import tempfile
import os

from app.core.database import Base, get_db
from main import app

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def client():
    # Create test database tables
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    # Clean up
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("test.db"):
        os.remove("test.db")

def test_root_endpoint(client):
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "StoryLens API is running!" in response.json()["message"]

def test_health_check(client):
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_get_stories_empty(client):
    """Test getting stories when none exist"""
    response = client.get("/api/stories")
    assert response.status_code == 200
    assert response.json() == []

def test_upload_no_file(client):
    """Test upload endpoint without file"""
    response = client.post("/api/upload")
    assert response.status_code == 422  # Validation error

def test_upload_invalid_file_type(client):
    """Test upload with invalid file type"""
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp:
        tmp.write(b"This is not an image")
        tmp.flush()
        
        with open(tmp.name, "rb") as f:
            response = client.post(
                "/api/upload",
                files={"file": ("test.txt", f, "text/plain")},
                data={"story_type": "story"}
            )
        
        os.unlink(tmp.name)
    
    assert response.status_code == 400
    assert "File must be an image" in response.json()["detail"] 