# Optimized SARCIS Quick Start Guide

## What's New? 🚀

### Performance Improvements
- ✅ **Efficient Multiprocessing**: Models load once per worker, not per file
- ✅ **Lower Memory Usage**: Optimal process count (max 4 workers)
- ✅ **Faster Processing**: Reuse pre-loaded models across all files
- ✅ **Multilingual Support**: Hindi/Hinglish with automatic translation
- ✅ **Incremental Analysis**: Only process new files
- ✅ **Audio Playback**: Listen to files with timestamp navigation

## Quick Start

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Install ffmpeg (Required for Whisper)
```bash
# Windows (using winget)
winget install ffmpeg

# After installation, restart your terminal
```

### 3. Setup Environment
Create `.env` file in backend directory:
```env
MONGO_URI=your_mongodb_connection_string
MONGODB_DB_NAME=sarcis
JWT_SECRET=your_secret_key_here
```

### 4. Start Backend
```bash
cd backend
python main.py
```

**First startup will be slower** as it initializes the database. Subsequent starts are faster.

### 5. Start Frontend
```bash
cd frontend
npm install
npm run dev
```

### 6. Access Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## How It Works

### File Processing Flow
```
1. Upload files → Status: pending
2. Click "Analyze" → Only processes pending files
3. Workers initialize → Load models once per worker
4. Process files → Reuse models for all files
5. Save results → Status: done
6. View results → Audio playback + insights
```

### Multiprocessing Architecture
```
Main Process
    │
    ├─ Worker 1 (loads models once)
    │   ├─ Process file_1.mp3
    │   ├─ Process file_5.mp3
    │   └─ Process file_9.mp3
    │
    ├─ Worker 2 (loads models once)
    │   ├─ Process file_2.mp3
    │   ├─ Process file_6.mp3
    │   └─ Process file_10.mp3
    │
    ├─ Worker 3 (loads models once)
    │   ├─ Process file_3.mp3
    │   └─ Process file_7.mp3
    │
    └─ Worker 4 (loads models once)
        ├─ Process file_4.mp3
        └─ Process file_8.mp3
```

## Usage Examples

### Basic Workflow
```bash
1. Create cluster: "Customer Complaints Q1"
2. Upload audio files: complaint_01.mp3, complaint_02.mp3
3. Click "Analyze" → Processes 2 files
4. Upload more files: complaint_03.mp3
5. Click "Analyze" → Only processes 1 new file (incremental!)
6. View results with audio playback
```

### Re-analysis (Force Reprocess)
```bash
POST /reanalyze/{cluster_id}
```
This will:
- Reset all file statuses to pending
- Delete existing results
- Reprocess all files from scratch

## Performance Tips

### 1. Optimal File Count
- **Best**: 10-20 files per batch
- **Good**: 5-50 files per batch
- **Avoid**: 100+ files in single batch (split into multiple clusters)

### 2. Audio File Format
- **Best**: MP3 (compressed, faster upload)
- **Good**: WAV (uncompressed, larger)
- **Supported**: MP3, WAV, M4A

### 3. System Resources
- **Minimum**: 4GB RAM, 2 CPU cores
- **Recommended**: 8GB RAM, 4 CPU cores
- **Optimal**: 16GB RAM, 8 CPU cores

### 4. Model Selection
Current: `base` (good balance)
- To change: Edit `processor.py` line with `whisper.load_model("base")`
- Options: `tiny`, `base`, `small`, `medium`, `large`

## Troubleshooting

### Issue: "ffmpeg not found"
```bash
# Install ffmpeg
winget install ffmpeg

# Restart terminal
# Restart backend
python main.py
```

### Issue: "Models loading slowly"
This is normal on first run per worker. Models are cached after first load.

### Issue: "High memory usage"
Reduce number of workers in `processor.py`:
```python
num_processes = min(2, max(1, cpu_count() // 2))  # Use 2 instead of 4
```

### Issue: "Translation not working"
Translation model downloads on first use. Check internet connection.

## API Endpoints

### Authentication
- `POST /auth/signup` - Create account
- `POST /auth/login` - Login

### Clusters
- `GET /clusters` - List clusters
- `POST /clusters` - Create cluster
- `DELETE /clusters/{id}` - Delete cluster

### Files
- `POST /upload` - Upload files
- `GET /clusters/{id}/files` - List files

### Analysis
- `POST /analyze/{id}` - Analyze (incremental)
- `POST /reanalyze/{id}` - Force reprocess all
- `GET /results/{id}` - Get results
- `GET /clusters/{id}/insights` - Get insights

### Audio
- `GET /audio/{cluster_id}/{filename}` - Stream audio file

## Features

### Multilingual Support
- Detects language automatically (Whisper)
- Translates Hindi/Hinglish to English
- Stores both original and translated text
- Runs NLP on translated text for accuracy

### Event Classification
- Complaint detection
- Urgency detection
- Financial issues
- Technical issues
- Escalation signals
- Risk signals
- Negative language

### Priority Scoring
- **Critical**: Risk signals, escalation + urgency
- **High**: Complaints + urgency
- **Medium**: Complaints or technical issues
- **Low**: General queries

### Incremental Analysis
- Only processes new files
- Skips already analyzed files
- Updates existing results if needed
- Fast repeated analysis

## Next Steps

1. Upload test audio files
2. Run analysis
3. View results with audio playback
4. Upload more files
5. Run analysis again (only new files processed!)

## Support

For issues or questions:
1. Check `MULTIPROCESSING_OPTIMIZATION.md` for technical details
2. Check `IMPROVEMENTS_SUMMARY.md` for feature overview
3. Check backend logs for error messages
4. Check API docs at http://localhost:8000/docs
