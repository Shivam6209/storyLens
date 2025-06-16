# StoryLens API Documentation

## Overview

The StoryLens API provides endpoints for uploading images and generating creative stories and poems using AI models. The API also supports audio narration generation and story management.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API does not require authentication. This may be added in future versions.

## Endpoints

### Health Check

#### GET `/health`

Check if the API is running.

**Response:**
```json
{
  "status": "healthy"
}
```

### Upload and Generate Story

#### POST `/api/upload`

Upload an image and generate a story with optional audio narration.

**Request:**
- Content-Type: `multipart/form-data`
- Body:
  - `file`: Image file (JPEG, PNG, WebP, max 10MB)
  - `story_type`: "story" or "poem" (optional, default: "story")

**Response:**
```json
{
  "id": "uuid-string",
  "story_text": "Generated story text...",
  "story_type": "story",
  "image_filename": "uuid_filename.jpg",
  "audio_filename": "uuid.wav",
  "audio_url": "/api/audio/uuid.wav",
  "created_at": "2024-01-01T00:00:00Z"
}
```

**Error Responses:**
- `400`: Invalid file type or size
- `500`: Story generation failed

### Get All Stories

#### GET `/api/stories`

Retrieve all generated stories with pagination.

**Query Parameters:**
- `skip`: Number of stories to skip (default: 0)
- `limit`: Maximum number of stories to return (default: 100)

**Response:**
```json
[
  {
    "id": "uuid-string",
    "story_text": "Generated story text...",
    "story_type": "story",
    "image_filename": "uuid_filename.jpg",
    "audio_filename": "uuid.wav",
    "audio_url": "/api/audio/uuid.wav",
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

### Get Single Story

#### GET `/api/stories/{story_id}`

Retrieve a specific story by ID.

**Response:**
```json
{
  "id": "uuid-string",
  "story_text": "Generated story text...",
  "story_type": "story",
  "image_filename": "uuid_filename.jpg",
  "audio_filename": "uuid.wav",
  "audio_url": "/api/audio/uuid.wav",
  "created_at": "2024-01-01T00:00:00Z"
}
```

**Error Responses:**
- `404`: Story not found

### Delete Story

#### DELETE `/api/stories/{story_id}`

Delete a story and its associated files.

**Response:**
```json
{
  "message": "Story deleted successfully"
}
```

**Error Responses:**
- `404`: Story not found

### Get Audio File

#### GET `/api/audio/{filename}`

Stream an audio file.

**Response:**
- Content-Type: `audio/wav`
- Body: Audio file stream

**Error Responses:**
- `404`: Audio file not found

### Get Image File

#### GET `/api/images/{filename}`

Get an uploaded image file.

**Response:**
- Content-Type: `image/*`
- Body: Image file

**Error Responses:**
- `404`: Image file not found

## Models Used

### Microsoft Kosmos-2
- **Model ID**: `microsoft/kosmos-2-patch14-224`
- **Purpose**: Multi-modal image-to-text generation
- **API**: Hugging Face Inference API

### Coqui XTTS-v2
- **Model Name**: `tts_models/multilingual/multi-dataset/xtts_v2`
- **Purpose**: Text-to-speech synthesis
- **Implementation**: Local inference

## Error Handling

All errors follow the FastAPI standard format:

```json
{
  "detail": "Error message description"
}
```

Common HTTP status codes:
- `200`: Success
- `400`: Bad Request (invalid input)
- `404`: Not Found
- `422`: Validation Error
- `500`: Internal Server Error

## Rate Limiting

Currently, no rate limiting is implemented. Consider implementing rate limiting for production use.

## File Limits

- **Maximum file size**: 10MB
- **Supported formats**: JPEG, PNG, WebP
- **Audio duration limit**: 300 seconds (5 minutes) 