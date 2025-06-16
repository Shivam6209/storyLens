# Environment Setup

Create a `.env` file in the root directory with the following variables:

```env
# API Configuration
API_BASE_URL=http://localhost:8000
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Hugging Face API (for Kosmos-2)
HUGGINGFACE_API_KEY=your_huggingface_api_key_here

# Database Configuration (PostgreSQL)
DB_HOST=your_db_host_here
DB_PORT=5432
DB_USERNAME=your_db_username_here
DB_PASSWORD=your_db_password_here
DB_DATABASE=your_db_name_here

# Example with your provided database:
# DB_HOST=schoolmangement-systemmangment9-b98a.i.aivencloud.com
# DB_PORT=18602
# DB_USERNAME=your_username
# DB_PASSWORD=your_password
# DB_DATABASE=foodShare

# Audio Settings
AUDIO_OUTPUT_DIR=./audio_files
MAX_AUDIO_DURATION=300

# File Upload Settings
MAX_FILE_SIZE=10485760  # 10MB
ALLOWED_EXTENSIONS=jpg,jpeg,png,webp

# Development Settings
DEBUG=true
LOG_LEVEL=INFO
```

## Frontend Environment

Create a `.env` file in the `frontend/` directory:

```env
VITE_API_BASE_URL=http://localhost:8000
```

## Getting API Keys

### Hugging Face API Key
1. Go to https://huggingface.co/
2. Sign up or log in
3. Go to Settings > Access Tokens
4. Create a new token with "Read" permissions
5. Copy the token and use it as `HUGGINGFACE_API_KEY`

### Database Setup
The application is configured to use PostgreSQL. You can use the provided database credentials or set up your own PostgreSQL instance.

## Quick Start

1. Copy the environment variables above into your `.env` files
2. Replace the placeholder values with your actual credentials
3. Follow the setup instructions in the main README.md 