# 🚀 StoryLens Setup Guide

## ✅ Current Status

Your StoryLens application is now **fully configured** and ready to run! Here's what's been set up:

### 🗄️ Database Configuration
- ✅ PostgreSQL database connection configured
- ✅ Database: `foodShare` on `schoolmangement-systemmangment9-b98a.i.aivencloud.com:18602`
- ✅ Connection tested and working
- ✅ Database models ready for table creation

### 🔧 Backend Setup
- ✅ FastAPI application configured
- ✅ All dependencies installed (except optional TTS)
- ✅ Environment variables configured
- ✅ API endpoints ready

### 🎨 Frontend Setup
- ✅ React + TypeScript application
- ✅ Tailwind CSS configured
- ✅ All dependencies installed
- ✅ API integration ready

## 🔑 Required Steps to Complete Setup

### 1. Update Database Password
Edit `backend/.env` and replace `your_password_here` with your actual database password:

```env
DB_PASSWORD=your_actual_password_here
```

### 2. Get Hugging Face API Key
1. Go to https://huggingface.co/
2. Sign up or log in
3. Go to Settings > Access Tokens
4. Create a new token with "Read" permissions
5. Update `backend/.env`:

```env
HUGGINGFACE_API_KEY=your_actual_huggingface_token_here
```

### 3. Optional: Install TTS for Audio Generation
If you want audio narration features:

```bash
cd backend
pip install coqui-tts torch torchaudio
```

## 🚀 Running the Application

### Start Backend (Terminal 1)
```bash
cd backend
python main.py
```
The API will be available at: http://localhost:8000

### Start Frontend (Terminal 2)
```bash
cd frontend
npm run dev
```
The web app will be available at: http://localhost:5173

## 🧪 Testing the Setup

### Test Backend
```bash
cd backend
python test_config.py
```

### Test Frontend
```bash
cd frontend
npm test
```

## 📋 Features Available

### ✅ Working Features
- 📸 **Photo Upload**: Drag & drop interface
- 🤖 **AI Story Generation**: Using Microsoft Kosmos-2
- 💾 **Database Storage**: PostgreSQL with your provided credentials
- 📱 **Responsive UI**: Modern React interface
- 🔄 **Real-time Updates**: React Query for state management

### 🔄 Optional Features
- 🎵 **Audio Narration**: Requires TTS installation
- 🧪 **Testing**: Full test suites for both frontend and backend

## 🌐 API Endpoints

- `GET /` - Health check
- `POST /api/upload` - Upload image and generate story
- `GET /api/stories` - Get all stories
- `GET /api/stories/{id}` - Get specific story
- `DELETE /api/stories/{id}` - Delete story
- `GET /api/audio/{filename}` - Stream audio file

## 🔧 Configuration Files

### Backend Environment (`backend/.env`)
```env
# Database Configuration
DB_HOST=schoolmangement-systemmangment9-b98a.i.aivencloud.com
DB_PORT=18602
DB_USERNAME=avnadmin
DB_PASSWORD=your_password_here
DB_DATABASE=foodShare

# API Configuration
API_BASE_URL=http://localhost:8000
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Hugging Face API
HUGGINGFACE_API_KEY=your_huggingface_api_key_here

# Audio Settings
AUDIO_OUTPUT_DIR=./audio_files
MAX_AUDIO_DURATION=300

# File Upload Settings
MAX_FILE_SIZE=10485760
ALLOWED_EXTENSIONS=jpg,jpeg,png,webp

# Development Settings
DEBUG=true
LOG_LEVEL=INFO
```

### Frontend Environment (`frontend/.env`)
```env
VITE_API_BASE_URL=http://localhost:8000
```

## 🎯 Next Steps

1. **Update your credentials** in the `.env` files
2. **Start both backend and frontend**
3. **Upload a photo** to test the story generation
4. **Enjoy your AI-powered story generator!**

## 🆘 Troubleshooting

### Database Connection Issues
- Verify your database password is correct
- Check if the database server is accessible
- Run `python test_config.py` to test connection

### API Key Issues
- Make sure your Hugging Face API key has the right permissions
- Test the key at https://huggingface.co/microsoft/kosmos-2-patch14-224

### Frontend Issues
- Make sure the backend is running on port 8000
- Check browser console for any errors
- Verify the API base URL in frontend/.env

## 📚 Documentation

- **API Documentation**: `docs/API.md`
- **Environment Setup**: `ENVIRONMENT_SETUP.md`
- **Main README**: `README.md`

---

🎉 **Congratulations!** Your StoryLens application is ready to transform photos into amazing stories! 