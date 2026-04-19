# Phase 2 Setup Guide
## Job Queue + Workers + Audio Processing

---

## What We've Built

✅ Redis job queue  
✅ Celery workers for background processing  
✅ Integration with existing audio pipeline (Whisper + NLP + GenAI)  
✅ Progress tracking  
✅ Results storage in MongoDB  
✅ Analytics computation  
✅ Job management API  

---

## Prerequisites

Before starting Phase 2, ensure Phase 1 is working:
- [ ] Backend running
- [ ] MongoDB connected
- [ ] Can create users and clusters
- [ ] Can upload files

---

## Installation Steps

### 1. Install New Dependencies

```bash
cd backend
pip install -r requirements.txt
```

New packages:
- `celery==5.3.4` - Task queue
- `redis==5.0.1` - Message broker
- `flower==2.0.1` - Monitoring tool

### 2. Install and Start Redis

#### Option A: Docker (Recommended)
```bash
docker run -d -p 6379:6379 --name redis redis:latest
```

#### Option B: Windows
Download from: https://github.com/microsoftarchive/redis/releases
```bash
redis-server
```

#### Option C: Linux/Mac
```bash
# Ubuntu/Debian
sudo apt-get install redis-server
sudo systemctl start redis

# Mac
brew install redis
brew services start redis
```

Verify Redis is running:
```bash
redis-cli ping
# Should return: PONG
```

### 3. Update Environment Variables

Your `.env` has been updated with:
```env
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1
CELERY_WORKERS=3
MAX_FILES_PER_JOB=1000
```

### 4. Start the System

You now need **3 processes** running:

#### Terminal 1: Backend API
```bash
cd backend
python main.py
```

#### Terminal 2: Celery Worker
```bash
cd backend

# Windows
start_worker.bat

# Linux/Mac
chmod +x start_worker.sh
./start_worker.sh
```

#### Terminal 3: Flower (Optional - Monitoring)
```bash
cd backend

# Linux/Mac
chmod +x start_flower.sh
./start_flower.sh

# Windows
celery -A queue.celery_app flower --port=5555
```

Access Flower at: `http://localhost:5555`

---

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Frontend (Next.js)                     │
└────────────────────────┬────────────────────────────────┘
                         │ HTTP + JWT
                         ▼
┌─────────────────────────────────────────────────────────┐
│                   FastAPI Backend                        │
│  POST /api/clusters/{id}/analyze                         │
│  GET  /api/jobs/{id}                                     │
│  GET  /api/clusters/{id}/results                         │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                    Redis Queue                           │
│  - Job queue                                             │
│  - Task results                                          │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                  Celery Workers (3)                      │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Worker 1: Process File A                        │   │
│  │  Worker 2: Process File B                        │   │
│  │  Worker 3: Process File C                        │   │
│  └──────────────────────────────────────────────────┘   │
│                         │                                │
│  ┌──────────────────────▼──────────────────────────┐   │
│  │  Audio Processing Pipeline                       │   │
│  │  1. Whisper Transcription                        │   │
│  │  2. NLP Analysis (Sentiment, Intent, Events)     │   │
│  │  3. GenAI Processing (High-priority segments)    │   │
│  │  4. Priority Assignment                          │   │
│  └──────────────────────┬──────────────────────────┘   │
└─────────────────────────┼────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    MongoDB                               │
│  - Store segments                                        │
│  - Update job progress                                   │
│  - Store analytics                                       │
└─────────────────────────────────────────────────────────┘
```

---

## New API Endpoints

### Job Management

#### Start Analysis Job
```bash
POST /api/clusters/{cluster_id}/analyze
Authorization: Bearer TOKEN
Body: {
  "file_ids": ["file1", "file2"]  # Optional, processes all if omitted
}

Response: {
  "job_id": "...",
  "cluster_id": "...",
  "status": "pending",
  "total_files": 10,
  "message": "Job queued successfully"
}
```

#### Get Job Status
```bash
GET /api/jobs/{job_id}
Authorization: Bearer TOKEN

Response: {
  "id": "...",
  "cluster_id": "...",
  "status": "running",
  "total_files": 10,
  "processed_files": 5,
  "progress": 50.0,
  "created_at": "...",
  "started_at": "...",
  "completed_at": null
}
```

#### List Jobs
```bash
GET /api/jobs?cluster_id=...&status=running
Authorization: Bearer TOKEN

Response: {
  "jobs": [...],
  "pagination": {...}
}
```

#### Cancel Job
```bash
POST /api/jobs/{job_id}/cancel
Authorization: Bearer TOKEN
```

### Results & Analytics

#### Get Cluster Segments
```bash
GET /api/clusters/{id}/segments?event=complaint&priority=high
Authorization: Bearer TOKEN

Response: {
  "segments": [
    {
      "id": "...",
      "start": 10.2,
      "end": 14.5,
      "text": "...",
      "events": ["complaint", "urgency"],
      "sentiment": "negative",
      "priority": "high"
    }
  ],
  "pagination": {...}
}
```

#### Get Cluster Analytics
```bash
GET /api/clusters/{id}/analytics
Authorization: Bearer TOKEN

Response: {
  "cluster_id": "...",
  "total_files": 100,
  "total_segments": 2500,
  "events": {
    "complaint": 800,
    "urgency": 500
  },
  "sentiment": {
    "positive": 500,
    "negative": 1000,
    "neutral": 1000
  },
  "priority": {
    "critical": 50,
    "high": 300,
    "medium": 800,
    "low": 1350
  }
}
```

#### Get Complete Results
```bash
GET /api/clusters/{id}/results
Authorization: Bearer TOKEN

Response: {
  "cluster": {...},
  "files": [
    {
      "id": "...",
      "filename": "call_001.wav",
      "segments": [...]
    }
  ],
  "analytics": {...}
}
```

---

## Testing Phase 2

### 1. Quick Test

```bash
# 1. Create cluster
curl -X POST http://localhost:8000/api/clusters \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Cluster"}'

# 2. Upload audio file
curl -X POST http://localhost:8000/api/clusters/CLUSTER_ID/upload \
  -H "Authorization: Bearer TOKEN" \
  -F "files=@test_audio.wav"

# 3. Start analysis
curl -X POST http://localhost:8000/api/clusters/CLUSTER_ID/analyze \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}'

# 4. Check progress
curl -X GET http://localhost:8000/api/jobs/JOB_ID \
  -H "Authorization: Bearer TOKEN"

# 5. View results
curl -X GET http://localhost:8000/api/clusters/CLUSTER_ID/results \
  -H "Authorization: Bearer TOKEN"
```

### 2. Monitor Workers

#### Check Celery Workers
```bash
celery -A queue.celery_app inspect active
celery -A queue.celery_app inspect stats
```

#### Check Redis Queue
```bash
redis-cli
> KEYS *
> LLEN celery
```

#### Use Flower UI
Open `http://localhost:5555` to see:
- Active workers
- Task progress
- Task history
- Worker statistics

---

## How It Works

### Processing Flow

1. **User uploads files** → Stored in `uploads/{cluster_id}/`
2. **User starts analysis** → Job created in MongoDB
3. **Job queued to Redis** → Celery picks it up
4. **Worker processes each file:**
   - Load audio file
   - Transcribe with Whisper
   - Analyze with NLP
   - Process high-priority segments with GenAI
   - Assign priorities
   - Store segments in MongoDB
   - Update progress
5. **Job completes** → Analytics computed
6. **User views results** → Fetch from MongoDB

### Task Types

**1. `process_audio_file`**
- Processes single audio file
- Runs Whisper + NLP + GenAI pipeline
- Stores segments in database
- Updates file status

**2. `process_cluster_job`**
- Orchestrates processing of multiple files
- Updates job progress
- Handles errors
- Triggers analytics computation

**3. `compute_cluster_analytics`**
- Aggregates all segments
- Computes statistics
- Stores in `cluster_analytics` collection

---

## File Structure

```
backend/
├── queue/                         [NEW]
│   ├── __init__.py
│   ├── celery_app.py             # Celery configuration
│   └── tasks.py                  # Processing tasks
│
├── routes/
│   ├── jobs.py                   [NEW] # Job management
│   └── analytics.py              [NEW] # Results & analytics
│
├── start_worker.sh               [NEW] # Start worker (Linux/Mac)
├── start_worker.bat              [NEW] # Start worker (Windows)
└── start_flower.sh               [NEW] # Start monitoring
```

---

## Configuration

### Celery Settings

Edit `backend/queue/celery_app.py`:

```python
# Worker settings
worker_prefetch_multiplier=1  # Process one task at a time
worker_max_tasks_per_child=50  # Restart after 50 tasks

# Task settings
task_time_limit=3600  # 1 hour max per task
task_soft_time_limit=3300  # 55 min soft limit
```

### Worker Concurrency

```bash
# Process 3 files simultaneously
celery -A queue.celery_app worker --concurrency=3

# Process 10 files simultaneously (more powerful machine)
celery -A queue.celery_app worker --concurrency=10
```

---

## Troubleshooting

### Redis Connection Error
```
Error: Cannot connect to Redis
```
**Solution:**
```bash
# Check if Redis is running
redis-cli ping

# Start Redis
docker start redis
# OR
redis-server
```

### Worker Not Starting
```
ModuleNotFoundError: No module named 'celery'
```
**Solution:**
```bash
pip install -r requirements.txt
```

### Tasks Not Processing
```
No workers available
```
**Solution:**
```bash
# Check workers
celery -A queue.celery_app inspect active

# Restart worker
# Stop with Ctrl+C, then restart
./start_worker.sh
```

### Audio Processing Fails
```
Error: Whisper model not loaded
```
**Solution:**
- Workers load models on first use
- Wait for "Audio processor initialized" log
- Check GPU/CPU availability

### Job Stuck in "pending"
**Solution:**
```bash
# Check worker logs
# Check Redis connection
# Restart worker
```

---

## Performance Tuning

### For Small Files (<1 min)
```bash
# More workers, less memory
celery -A queue.celery_app worker --concurrency=10
```

### For Large Files (>5 min)
```bash
# Fewer workers, more memory
celery -A queue.celery_app worker --concurrency=2
```

### For Production
```bash
# Multiple worker processes
celery -A queue.celery_app worker \
  --concurrency=5 \
  --max-tasks-per-child=100 \
  --loglevel=warning
```

---

## Monitoring

### Logs

**Backend logs:**
```bash
# In backend terminal
# Shows API requests
```

**Worker logs:**
```bash
# In worker terminal
# Shows task processing
```

**Flower dashboard:**
```
http://localhost:5555
```

### Metrics to Watch

- Tasks per minute
- Average task duration
- Failed tasks
- Worker CPU/memory usage
- Queue length

---

## Scaling

### Horizontal Scaling

Run multiple workers:

```bash
# Terminal 1
celery -A queue.celery_app worker --hostname=worker1@%h

# Terminal 2
celery -A queue.celery_app worker --hostname=worker2@%h

# Terminal 3
celery -A queue.celery_app worker --hostname=worker3@%h
```

### Queue Prioritization

```python
# High priority
process_audio_file.apply_async(args=[...], priority=9)

# Low priority
process_audio_file.apply_async(args=[...], priority=1)
```

---

## Next Steps

Once Phase 2 is working:

1. **Test with real audio files**
2. **Monitor performance**
3. **Adjust worker concurrency**
4. **Move to Phase 3: Frontend updates**

---

## Verification Checklist

- [ ] Redis is running
- [ ] Backend API is running
- [ ] Celery worker is running
- [ ] Can start analysis job
- [ ] Job status updates
- [ ] Files are processed
- [ ] Segments stored in MongoDB
- [ ] Analytics computed
- [ ] Can view results

---

**Phase 2 Complete!** 🎉

You now have:
- Background job processing
- Scalable worker system
- Progress tracking
- Full audio analysis pipeline
- Results storage
- Analytics computation

**Next: Phase 3 - Frontend Updates**
