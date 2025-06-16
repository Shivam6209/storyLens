# StoryLens - Multi-modal Photo Story Generator

StoryLens is an AI-powered application that transforms your photos into creative stories and poems with audio narration. Upload any photo and watch as AI generates an engaging narrative inspired by your image, complete with voice narration for sharing.

## Features

- 📸 **Photo Upload**: Support for various image formats (JPEG, PNG, WebP)
- 🤖 **AI Story Generation**: Powered by Microsoft's Kosmos-2 model for creative storytelling
- 🎵 **Audio Narration**: Text-to-speech using Coqui's XTTS-v2 model
- 📱 **Responsive Design**: Modern, mobile-friendly interface
- 💾 **Story Management**: Save and manage your generated stories
- 🔊 **Audio Playback**: Built-in audio player for generated narrations

## Tech Stack

### Frontend
- **React 18** with TypeScript
- **Tailwind CSS** for styling
- **Vite** for build tooling
- **React Query** for API state management
- **React Hook Form** for form handling

### Backend
- **FastAPI** (Python)
- **Microsoft Kosmos-2** for image-to-text generation
- **Coqui XTTS-v2** for text-to-speech
- **SQLite** for data storage
- **Pydantic** for data validation

## Prerequisites

- Node.js 18+ and npm
- Python 3.9+
- Git

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd storyLens
```

### 2. Environment Setup

Copy the environment template and fill in your API keys:

```bash
cp .env.example .env
```

Edit `.env` with your configuration (see Environment Variables section below).

### 3. Backend Setup

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 4. Frontend Setup

```bash
cd frontend
npm install
```

### 5. Run the Application

**Start Backend (from backend directory):**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Start Frontend (from frontend directory):**
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# API Configuration
API_BASE_URL=http://localhost:8000
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Hugging Face API (for Kosmos-2)
HUGGINGFACE_API_KEY=your_huggingface_api_key_here

# Database
DATABASE_URL=sqlite:///./storylens.db

# Audio Settings
AUDIO_OUTPUT_DIR=./audio_files
MAX_AUDIO_DURATION=300

# File Upload Settings
MAX_FILE_SIZE=10485760  # 10MB
ALLOWED_EXTENSIONS=jpg,jpeg,png,webp
```

## API Endpoints

### POST `/api/upload`
Upload an image and generate a story with audio narration.

**Request:**
- `file`: Image file (multipart/form-data)
- `story_type`: "story" or "poem" (optional, default: "story")

**Response:**
```json
{
  "id": "story_uuid",
  "story_text": "Generated story...",
  "audio_url": "/api/audio/story_uuid.wav",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### GET `/api/stories`
Retrieve all generated stories.

### GET `/api/stories/{story_id}`
Retrieve a specific story by ID.

### GET `/api/audio/{filename}`
Stream audio file.

## Models Used

### 1. Microsoft Kosmos-2
- **Purpose**: Multi-modal image-to-text generation
- **Capabilities**: Understands images and generates creative narratives
- **API**: Hugging Face Inference API
- **Model ID**: `microsoft/kosmos-2-patch14-224`

### 2. Coqui XTTS-v2
- **Purpose**: Text-to-speech synthesis
- **Capabilities**: High-quality voice synthesis with emotion
- **Implementation**: Local inference via Coqui TTS library
- **Voice**: Configurable (default: neutral English voice)

## Project Structure

```
storyLens/
├── frontend/                 # React frontend
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/          # Page components
│   │   ├── hooks/          # Custom React hooks
│   │   ├── services/       # API services
│   │   ├── types/          # TypeScript type definitions
│   │   └── utils/          # Utility functions
│   ├── public/             # Static assets
│   └── tests/              # Frontend tests
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Core functionality
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utility functions
│   ├── tests/              # Backend tests
│   └── requirements.txt    # Python dependencies
├── docs/                   # Documentation
└── .env.example           # Environment template
```

## Testing

### Frontend Tests
```bash
cd frontend
npm test
```

### Backend Tests
```bash
cd backend
pytest
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Microsoft for the Kosmos-2 model
- Coqui for the XTTS-v2 text-to-speech model
- Hugging Face for model hosting and inference APIs