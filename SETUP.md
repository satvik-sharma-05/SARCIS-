# 🚀 SARCIS Setup Guide

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.9 or higher
- Node.js 18 or higher
- FFmpeg (for audio processing)
- pip (Python package manager)
- npm or yarn

## Installation Steps

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd sarcis
```

### 2. Backend Setup

#### Install Python Dependencies

```bash
cd backend
pip install -r ../requirements.txt
```

#### Install FFmpeg

**Windows:**
```bash
# Using Chocolatey
choco install ffmpeg

# Or download from: https://ffmpeg.org/download.html
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt update
sudo apt install ffmpeg
```

#### Configure Environment Variables

Edit the `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
WHISPER_MODEL=base
LLM_MODEL=llama-3.1-70b-versatile
ENABLE_GENAI=true
MAX_SEGMENTS_PER_CALL=10
BATCH_SIZE=5
```

**Get Groq API Key:**
1. Visit https://console.groq.com
2. Sign up for a free account
3. Generate an API key
4. Copy and paste it into `.env`

### 3. Frontend Setup

```bash
cd frontend
npm install
```

## Running the Application

### Start Backend Server

```bash
cd backend
python main.py
```

The backend will start on `http://localhost:8000`

### Start Frontend Development Server

Open a new terminal:

```bash
cd frontend
npm run dev
```

The frontend will start on `http://localhost:3000`

## Testing the Application

### 1. Prepare Test Audio

Create a `test_audio` folder and add sample audio files:
- `.wav` files
- `.mp3` files
- `.m4a` files

### 2. Upload and Analyze

1. Open `http://localhost:3000` in your browser
2. Click "Upload Audio" or navigate to `/upload`
3. Drag and drop audio files or browse to select
4. Click "Analyze Audio"
5. Wait for processing (may take 30-60 seconds per file)
6. View results on the results page

## API Endpoints

### Health Check
```bash
GET http://localhost:8000/health
```

### Analyze Multiple Files
```bash
POST http://localhost:8000/api/analyze
Content-Type: multipart/form-data
Body: files (multiple audio files)
```

### Analyze Single File
```bash
POST http://localhost:8000/api/analyze-single
Content-Type: multipart/form-data
Body: file (single audio file)
```

## Troubleshooting

### Backend Issues

**Whisper Model Download:**
- First run will download the Whisper model (~140MB for base model)
- This is automatic but requires internet connection

**CUDA/GPU Issues:**
- The system works on CPU by default
- For GPU acceleration, install PyTorch with CUDA support

**Import Errors:**
```bash
pip install --upgrade -r requirements.txt
```

### Frontend Issues

**Port Already in Use:**
```bash
# Change port in package.json
"dev": "next dev -p 3001"
```

**Module Not Found:**
```bash
rm -rf node_modules package-lock.json
npm install
```

### API Connection Issues

**CORS Errors:**
- Ensure backend is running on port 8000
- Check `FRONTEND_URL` in `.env`

**Timeout Errors:**
- Large audio files may take longer
- Increase timeout in axios config

## Performance Optimization

### For Faster Processing:

1. **Use Smaller Whisper Model:**
   ```env
   WHISPER_MODEL=tiny  # Fastest, less accurate
   ```

2. **Disable GenAI:**
   ```env
   ENABLE_GENAI=false  # Use only NLP layer
   ```

3. **Reduce Batch Size:**
   ```env
   BATCH_SIZE=3
   ```

### For Better Accuracy:

1. **Use Larger Whisper Model:**
   ```env
   WHISPER_MODEL=medium  # More accurate, slower
   ```

2. **Enable GenAI:**
   ```env
   ENABLE_GENAI=true
   ```

## Production Deployment

### Backend (FastAPI)

```bash
# Install production server
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

### Frontend (Next.js)

```bash
# Build for production
npm run build

# Start production server
npm start
```

## System Requirements

### Minimum:
- 4GB RAM
- 2 CPU cores
- 5GB disk space

### Recommended:
- 8GB RAM
- 4 CPU cores
- 10GB disk space
- GPU (optional, for faster processing)

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review logs in terminal
3. Open an issue on GitHub

## Next Steps

After setup:
1. Test with sample audio files
2. Customize event detection keywords in `nlp_engine.py`
3. Adjust UI theme in `tailwind.config.ts`
4. Add custom features as needed

Happy analyzing! 🎧
