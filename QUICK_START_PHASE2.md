# 🚀 Quick Start - Phase 2
## Job Queue + Workers + Audio Processing

---

## Installation (5 minutes)

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Start Redis
```bash
# Docker (recommended)
docker run -d -p 6379:6379 --name redis redis:latest

# Verify
redis-cli ping  # Should return: PONG
```

### 3. Start 3 Processes

#### Terminal 1: Backend
```bash
cd backend
python main.py
```

#### Terminal 2: Worker
```bash
cd backend

# Windows
start_worker.bat

# Linux/Mac
chmod +x start_worker.sh
./start_worker.sh
```

#### Terminal 3: Flower (Optional)
```bash
cd backend
chmod +x start_flower.sh
./start_flower.sh

# Open http://localhost:5555
```

---

## Test It (3 minutes)

### Automated Test
```bash
# Add audio file to test_audio/ first
python test_phase2.py
```

### Manual Test

1. **Create cluster** (from Phase 1)
2. **Upload audio file**
3. **Start analysis:**
```bash
curl -X POST http://localhost:8000/api/clusters/CLUSTER_ID/analyze \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}'
```

4. **Check progress:**
```bash
curl -X GET http://localhost:8000/api/jobs/JOB_ID \
  -H "Authorization: Bearer TOKEN"
```

5. **View results:**
```bash
curl -X GET http://localhost:8000/api/clusters/CLUSTER_ID/results \
  -H "Authorization: Bearer TOKEN"
```

---

## Quick API Reference

### Start Analysis
```bash
POST /api/clusters/{id}/analyze
Authorization: Bearer TOKEN
Body: { "file_ids": ["..."] }  # Optional

Response: {
  "job_id": "...",
  "status": "pending",
  "total_files": 10
}
```

### Check Progress
```bash
GET /api/jobs/{job_id}
Authorization: Bearer TOKEN

Response: {
  "status": "running",
  "progress": 50.0,
  "processed_files": 5,
  "total_files": 10
}
```

### View Results
```bash
GET /api/clusters/{id}/results
Authorization: Bearer TOKEN

Response: {
  "cluster": {...},
  "files": [
    {
      "filename": "audio.wav",
      "segments": [...]
    }
  ],
  "analytics": {...}
}
```

### Get Analytics
```bash
GET /api/clusters/{id}/analytics
Authorization: Bearer TOKEN

Response: {
  "total_segments": 2500,
  "events": {
    "complaint": 800,
    "urgency": 500
  },
  "sentiment": {...},
  "priority": {...}
}
```

---

## What You Can Do Now

✅ Upload audio files  
✅ Start background analysis jobs  
✅ Track progress in real-time  
✅ View transcription segments  
✅ See sentiment & intent analysis  
✅ Get event detection (complaints, urgency, etc.)  
✅ View aggregated analytics  
✅ Monitor workers with Flower  

---

## How It Works

```
1. Upload files → Stored in uploads/
2. Start job → Queued to Redis
3. Worker picks up → Processes with Whisper + NLP + GenAI
4. Stores segments → MongoDB
5. Computes analytics → Aggregated stats
6. View results → API endpoints
```

---

## Monitoring

### Flower Dashboard
```
http://localhost:5555
```

Shows:
- Active workers
- Task progress
- Success/failure rates
- Worker stats

### Check Workers
```bash
celery -A queue.celery_app inspect active
celery -A queue.celery_app inspect stats
```

### Check Redis
```bash
redis-cli
> KEYS *
> LLEN celery
```

---

## Troubleshooting

**Redis not running?**
```bash
docker start redis
# OR
redis-server
```

**Worker not processing?**
```bash
# Check worker logs in Terminal 2
# Restart worker: Ctrl+C then restart
./start_worker.sh
```

**Job stuck?**
```bash
# Check job status
GET /api/jobs/{job_id}

# Check worker logs
# Cancel and retry
POST /api/jobs/{job_id}/cancel
```

**Import errors?**
```bash
pip install -r requirements.txt
```

---

## Performance

| Workers | Files/Hour | Concurrent |
|---------|------------|------------|
| 1 | ~120 | 1 file |
| 3 | ~360 | 3 files |
| 5 | ~600 | 5 files |

Processing time: ~0.5x audio duration

---

## File Structure

```
backend/
├── queue/              ← Celery tasks
│   ├── celery_app.py
│   └── tasks.py
├── routes/
│   ├── jobs.py         ← Job management
│   └── analytics.py    ← Results & analytics
├── start_worker.sh     ← Start worker
└── start_flower.sh     ← Start monitoring
```

---

## What's Next?

**Phase 3: Frontend Updates**
- Login/signup UI
- Cluster management
- File upload interface
- Progress tracking
- Results visualization
- Analytics dashboard

---

## Need Help?

1. **Setup Issues** → `PHASE2_SETUP.md`
2. **Architecture** → `PHASE2_COMPLETE.md`
3. **API Reference** → `API_SPEC.md`
4. **Full Roadmap** → `IMPLEMENTATION_ROADMAP.md`

---

**Phase 2 Complete!** 🎉

You now have:
- Background processing
- Scalable workers
- Progress tracking
- Full audio analysis
- Results storage
- Analytics

**Ready for Phase 3?** 🚀
