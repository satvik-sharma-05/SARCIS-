# SARCIS Quick Reference Guide

## 🚀 Quick Start

### Backend
```bash
cd backend
python main.py
```
**URL**: http://localhost:8000

### Frontend
```bash
cd frontend
npm install  # First time only
npm run dev
```
**URL**: http://localhost:3000

## 📊 Features Overview

### 1. Multiprocessing Optimization
- Models load once per worker
- Efficient resource usage
- Fast processing after initial load
- Max 4 workers (configurable)

### 2. Multilingual Support
- Auto-detects language (Whisper)
- Translates Hindi/Hinglish to English
- Accurate NLP on translated text
- Stores both original and translated

### 3. Incremental Analysis
- Only processes new files
- Skips already analyzed files
- Fast repeated analysis
- Status tracking (pending → processing → done)

### 4. Audio Playback
- Stream audio files
- Click segments to jump to timestamp
- Native HTML5 controls

### 5. Cluster Insights & Analytics
- Visual charts (pie, bar)
- File rankings by importance
- Risk signal detection
- Comprehensive metrics

## 🎯 User Workflow

```
1. Sign Up / Login
   ↓
2. Create Cluster
   ↓
3. Upload Audio Files
   ↓
4. Run Analysis
   ↓
5. View Results (detailed segments)
   ↓
6. View Insights (analytics dashboard)
```

## 🔌 API Endpoints

### Authentication
```
POST /auth/signup
POST /auth/login
```

### Clusters
```
GET    /clusters
POST   /clusters
DELETE /clusters/{id}
```

### Files
```
POST /upload
GET  /clusters/{id}/files
```

### Analysis
```
POST /analyze/{id}        # Incremental (only new files)
POST /reanalyze/{id}      # Force reprocess all
GET  /results/{id}        # Detailed results
GET  /clusters/{id}/insights  # Analytics
```

### Audio
```
GET /audio/{cluster_id}/{filename}
```

## 📈 Insights Metrics

### Key Metrics
- Total Files
- Total Segments
- Complaint %
- Urgency %
- Negative %
- High Priority %

### Charts
- Sentiment Distribution (Pie)
- Priority Distribution (Pie)
- Event Distribution (Bar)
- Top Issues (Horizontal Bar)

### File Ranking Formula
```
score = (
    complaint_count × 2 +
    urgency_count × 3 +
    escalation_count × 4 +
    negative_count × 1.5 +
    high_priority_count × 2 +
    risk_count × 5
)
```

## 🎨 Event Types

- `complaint` - Customer complaints
- `urgency` - Time-sensitive requests
- `request` - General requests
- `financial_issue` - Payment/refund related
- `technical_issue` - Technical problems
- `positive_feedback` - Positive comments
- `escalation` - Legal threats, manager requests
- `negative_language` - Abuse, anger
- `risk_signal` - Security threats

## 🎯 Intent Types

- `technical_issue` - Technical problems
- `payment_issue` - Payment related
- `refund_request` - Refund requests
- `account_issue` - Account/login issues
- `help_request` - Help needed
- `feature_request` - Feature suggestions
- `general_query` - General questions

## 🚨 Priority Levels

- `critical` - Score ≥ 7 (immediate action)
- `high` - Score ≥ 4 (urgent)
- `medium` - Score ≥ 2 (normal)
- `low` - Score < 2 (low priority)

## 🔧 Configuration

### Process Count
Edit `backend/services/processor.py`:
```python
num_processes = min(4, max(1, cpu_count() // 2))
# Change 4 to your desired max
```

### Whisper Model
Edit `backend/services/processor.py`:
```python
whisper_model = whisper.load_model("base")
# Options: tiny, base, small, medium, large
```

### Importance Score Weights
Edit `backend/main.py` in insights endpoint:
```python
score = (
    complaint_count * 2,      # Change weight
    urgency_count * 3,        # Change weight
    escalation_count * 4,     # Change weight
    negative_count * 1.5,     # Change weight
    high_priority_count * 2,  # Change weight
    risk_count * 5            # Change weight
)
```

## 📁 Project Structure

```
SARCIS/
├── backend/
│   ├── main.py              # FastAPI app
│   ├── db.py                # MongoDB connection
│   ├── models.py            # Data models
│   ├── services/
│   │   ├── auth.py          # Authentication
│   │   └── processor.py     # Audio processing
│   └── uploads/             # Audio files
│
├── frontend/
│   ├── app/
│   │   ├── dashboard/       # Dashboard page
│   │   ├── cluster/[id]/    # Cluster page
│   │   ├── results/[id]/    # Results page
│   │   └── insights/[id]/   # Insights page
│   └── lib/
│       ├── api.ts           # API client
│       └── auth-context.tsx # Auth context
│
└── Documentation/
    ├── MULTIPROCESSING_OPTIMIZATION.md
    ├── IMPROVEMENTS_SUMMARY.md
    ├── INSIGHTS_FEATURE.md
    └── ANALYTICS_COMPLETE.md
```

## 🐛 Troubleshooting

### ffmpeg not found
```bash
winget install ffmpeg
# Restart terminal
```

### Models loading slowly
- Normal on first run per worker
- Models are cached after first load

### High memory usage
- Reduce process count in processor.py
- Use smaller Whisper model (tiny or base)

### Translation not working
- Translation model downloads on first use
- Check internet connection

### Charts not displaying
```bash
cd frontend
npm install
npm run dev
```

### No insights available
- Run analysis on cluster first
- Check if results exist in MongoDB

## 📚 Documentation Files

- `MULTIPROCESSING_OPTIMIZATION.md` - Technical deep dive
- `IMPROVEMENTS_SUMMARY.md` - Feature overview
- `INSIGHTS_FEATURE.md` - Analytics documentation
- `ANALYTICS_COMPLETE.md` - Implementation summary
- `OPTIMIZED_QUICKSTART.md` - Getting started guide
- `QUICK_REFERENCE.md` - This file

## 🎯 Performance Tips

1. **Batch Size**: 10-20 files per cluster (optimal)
2. **File Format**: MP3 (compressed, faster)
3. **System**: 8GB RAM, 4 CPU cores (recommended)
4. **Model**: Use "base" for balance of speed/accuracy

## 🔐 Security

- JWT authentication
- User-specific data isolation
- File access control
- MongoDB connection string in .env

## 📊 Status Indicators

### File Status
- `pending` - Uploaded, not processed
- `processing` - Currently analyzing
- `done` - Successfully processed
- `failed` - Processing failed

### Cluster Status
- `active` - Ready for files
- `processing` - Analysis in progress
- `completed` - Analysis done
- `failed` - Analysis failed

## 🎉 Key Features Summary

✅ Efficient multiprocessing with model reuse
✅ Multilingual support (Hindi/Hinglish)
✅ Incremental analysis (only new files)
✅ Audio playback with timestamps
✅ Visual analytics dashboard
✅ File importance rankings
✅ Risk signal detection
✅ Simple, readable code
✅ Fast performance
✅ Comprehensive documentation

---

**Need Help?** Check the detailed documentation files or review the code comments!
