# 🧠 SARCIS - System Architecture

## 🚀 Final System Overview

**Cluster-based Audio Intelligence Platform with Parallel Processing**

### What It Does
- Upload audio files → organize into clusters
- Process files in parallel using multiprocessing
- Extract multi-layered timestamped insights
- Display interactive results with audio playback

---

## 🧩 Tech Stack

### 🌐 Frontend
- **Next.js 14** - React framework
- **Tailwind CSS** - Styling
- **Framer Motion** - Animations
- **WaveSurfer.js** - Audio visualization & playback
- **Axios** - API client

### 🧠 Backend
- **FastAPI** - High-performance Python API
- **Python multiprocessing** - Parallel file processing

### 🗄️ Database
- **MongoDB** - Document storage (clusters, files, results, insights)

### 🎧 AI Layer
- **OpenAI Whisper** - Audio transcription
- **Hugging Face Transformers** - NLP (sentiment, classification)
- **Custom Rules** - Event detection, priority assignment

### 💾 Storage
- **Local filesystem** - `/uploads` folder for audio files

### 🚀 Deployment
- **Frontend** → Vercel
- **Backend** → Render / Railway
- **Database** → MongoDB Atlas (free tier)

---

## 🏗️ System Architecture

```
Frontend (Next.js)
         ↓
FastAPI Backend
         ↓
MongoDB (clusters, files, results, insights)
         ↓
Local File Storage (/uploads)
         ↓
Multiprocessing Engine (4 parallel workers)
         ↓
AI Pipeline (Whisper + NLP + Rules)
         ↓
Results stored → MongoDB
         ↓
Frontend fetches & displays
```

---

## 🧩 Core Concepts

### 🔷 Cluster
A collection of audio files (like a project)
- Example: "Customer Calls", "Sales Calls"

### 📂 File
Individual audio file within a cluster
- Formats: .wav, .mp3, .m4a

### 🧠 Segment
Small chunk of audio with timestamp
- Contains: start time, end time, text, insights

### 📊 Result
AI-generated insights for each segment

### 📈 Cluster Insights
Aggregated analytics across all files in a cluster

---

## 🔄 Complete Workflow

### 1. User Creates Cluster
```
Frontend: POST /clusters
Backend: Stores in MongoDB
```

### 2. User Uploads Files
```
Frontend: Drag & drop files
Backend: 
  - Saves files → /uploads/{cluster_id}/
  - Stores metadata → MongoDB
```

### 3. User Clicks "Run Analysis"
```
Frontend: POST /analyze/{cluster_id}
Backend: Starts parallel processing
```

### 4. Backend Parallel Processing

```python
from multiprocessing import Pool

# Split files into batches
batch_size = 20

# Process in parallel (4 workers)
with Pool(processes=4) as pool:
    results = pool.map(process_file, files)
```

### 5. AI Pipeline (Per File)

#### Step 1: Transcription (Whisper)
```python
result = whisper_model.transcribe(audio_file)
# Output: [{"start": 10.2, "end": 14.5, "text": "..."}]
```

#### Step 2: NLP Analysis (Transformers)
```python
# Sentiment
sentiment = sentiment_analyzer(text)  # positive/negative

# Events (multi-label)
events = classify_events(text)  # complaint, urgency, etc.

# Intent
intent = detect_intent(text)  # refund_request, technical_issue, etc.
```

#### Step 3: Priority Logic
```python
if "urgent" in events and sentiment == "negative":
    priority = "critical"
elif "complaint" in events:
    priority = "high"
```

#### Step 4: Risk Detection
```python
if "sue" in text or "legal" in text:
    risk_signals.append("legal_threat")
```

### 6. Store Results
```json
{
  "file_id": "...",
  "segments": [
    {
      "start": 10.2,
      "end": 14.5,
      "text": "This is not working, fix it now!",
      "events": ["complaint", "urgency"],
      "sentiment": "negative",
      "intent": "technical_issue",
      "priority": "high",
      "keywords": ["not working", "fix"],
      "risk_signals": [],
      "confidence": 0.87
    }
  ],
  "summary": {
    "total_segments": 45,
    "negative_percentage": 60.5,
    "high_priority_count": 12,
    "top_issue": "complaint",
    "overall_sentiment": "negative"
  }
}
```

### 7. Calculate Cluster Insights
```json
{
  "cluster_id": "...",
  "total_files": 100,
  "total_segments": 4500,
  "complaint_percentage": 45.2,
  "urgency_percentage": 23.1,
  "negative_percentage": 38.7,
  "high_priority_percentage": 15.3,
  "top_events": {
    "complaint": 2034,
    "request": 1523,
    "urgency": 1040
  },
  "top_intents": {
    "technical_issue": 1800,
    "refund_request": 900
  }
}
```

### 8. Frontend Displays Results
- Interactive segment list
- Click segment → audio jumps to timestamp
- Visual insights dashboard
- Cluster-level analytics

---

## 🔥 Multi-Layered Insights

### 1. 🎯 Event Detection (Multi-Label)
- `complaint` - Issue/problem mentioned
- `urgency` - Time-sensitive request
- `request` - User asking for something
- `financial_issue` - Payment/refund related
- `technical_issue` - Bug/error mentioned
- `positive_feedback` - Appreciation/thanks
- `escalation` - Manager/legal mentioned
- `negative_language` - Harsh words

### 2. 😊 Sentiment Analysis
- `positive` - Happy/satisfied tone
- `negative` - Frustrated/angry tone
- `neutral` - Informational

### 3. 🧠 Intent Detection
- `refund_request` - Wants money back
- `technical_issue` - Something broken
- `help_request` - Needs assistance
- `account_issue` - Login/access problem
- `feature_request` - Wants new feature
- `general_query` - General question

### 4. ⚡ Priority/Severity
- `critical` - Immediate action required
- `high` - Important, needs attention
- `medium` - Standard priority
- `low` - Can wait

### 5. 🚨 Risk Signals
- `legal_threat` - Mentions lawsuit/lawyer
- `escalation_risk` - Wants to escalate
- `fraud_allegation` - Claims fraud/scam
- `reputation_risk` - Threatens bad review

### 6. 🧾 Keywords
- Extracted important phrases
- Example: ["not working", "urgent", "refund"]

### 7. 📊 Confidence Score
- 0.0 to 1.0
- How confident the AI is

### 8. 📈 Cluster Analytics
- Aggregated metrics across all files
- Trends and patterns
- Top issues and intents

---

## ⚡ Performance Design

### Why Fast?
- **Parallel processing** - 4 workers simultaneously
- **Batch execution** - Process multiple files at once
- **No blocking** - Async operations
- **Efficient models** - Optimized Whisper (base model)

### Real Performance
| Files | Time (Estimated) |
|-------|------------------|
| 50    | 5-10 min         |
| 100   | 10-20 min        |
| 500   | ~1 hour          |

### Optimization
- Limit processes to 4 (avoid CPU overload)
- Use smaller Whisper model (base vs large)
- Skip GenAI for simple segments
- Batch database operations

---

## ⚠️ Limitations (Clear & Honest)

### What This System IS
✅ Fast parallel processing (4-6 files at once)
✅ Multi-layered AI insights
✅ Scalable to hundreds of files
✅ Production-ready MVP
✅ Free to run locally

### What This System IS NOT
❌ Distributed system (no Kubernetes/Docker Swarm)
❌ Real-time processing (batch-based)
❌ Infinite scalability (CPU-bound)
❌ Cloud-native (runs on single machine)

### Trade-offs
- **CPU-bound** - Limited by machine cores
- **Not distributed** - Single server processing
- **Batch processing** - Not streaming/real-time

---

## 🚀 Why This Architecture is Perfect

### ✅ Pros
- **Fast** - Parallel processing
- **Simple** - No Redis, Celery, Docker
- **Free** - No cloud costs for processing
- **Deployable** - Works on Render/Railway
- **Scalable** - Handles 100s of files efficiently
- **Production-ready** - Real insights, not toy project

### ❌ Cons
- Not for 10,000+ files simultaneously
- Requires decent CPU (4+ cores recommended)
- Not real-time streaming

---

## 🎯 Interview Explanation

### One-Liner
> "The system uses Python multiprocessing to parallelize audio analysis, processing multiple files simultaneously while extracting multi-layered insights including sentiment, intent, events, and risk signals—all without requiring distributed infrastructure."

### Technical Deep-Dive
> "We built a cluster-based audio intelligence platform that processes audio files in parallel using Python's multiprocessing module. Each file goes through a pipeline: Whisper for transcription, Transformers for NLP analysis, and custom rules for event detection and priority assignment. The system extracts 8 layers of insights per segment and aggregates them into cluster-level analytics. It's designed to be fast (4 parallel workers), simple (no Redis/Celery), and deployable (runs on single server)."

### Architecture Highlight
> "The key innovation is the parallel processing layer—we use multiprocessing to handle 4 files simultaneously, which gives us near-linear speedup without the complexity of distributed systems. Combined with efficient AI models and batch database operations, we can process 100 files in under 20 minutes on a standard server."

---

## 📊 Database Schema

### Collections

#### `users`
```json
{
  "_id": "ObjectId",
  "email": "user@example.com",
  "name": "John Doe",
  "password": "hashed",
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### `clusters`
```json
{
  "_id": "ObjectId",
  "user_id": "ObjectId",
  "name": "Customer Calls",
  "created_at": "2024-01-01T00:00:00Z",
  "status": "completed"
}
```

#### `files`
```json
{
  "_id": "ObjectId",
  "cluster_id": "ObjectId",
  "file_name": "call_001.mp3",
  "file_path": "/uploads/cluster_id/call_001.mp3",
  "uploaded_at": "2024-01-01T00:00:00Z",
  "status": "completed"
}
```

#### `results`
```json
{
  "_id": "ObjectId",
  "cluster_id": "ObjectId",
  "file_id": "ObjectId",
  "file_name": "call_001.mp3",
  "segments": [...],
  "summary": {...}
}
```

#### `cluster_insights`
```json
{
  "_id": "ObjectId",
  "cluster_id": "ObjectId",
  "total_files": 100,
  "total_segments": 4500,
  "complaint_percentage": 45.2,
  "top_events": {...},
  "priority_distribution": {...}
}
```

---

## 🔥 Final System Flow

```
User
  ↓
Create Cluster
  ↓
Upload Files (drag & drop)
  ↓
Click "Run Analysis"
  ↓
Multiprocessing Engine (4 workers)
  ↓
AI Pipeline (Whisper + NLP + Rules)
  ↓
Store Results → MongoDB
  ↓
Calculate Cluster Insights
  ↓
Frontend Fetches & Displays
  ↓
User Clicks Segment → Audio Jumps to Timestamp
```

---

## 🎓 What You Built

✅ **AI system** - Real ML/NLP pipeline
✅ **Scalable design** - Parallel processing
✅ **Production workflow** - Complete user flow
✅ **Multi-layered insights** - Not just "threat detection"
✅ **Interview-ready** - Can explain architecture clearly

---

## 📚 Next Steps (Optional Enhancements)

1. **Add GenAI** - Use Groq for complex segment analysis
2. **Audio playback** - Integrate WaveSurfer.js fully
3. **Export results** - CSV/PDF download
4. **Real-time progress** - WebSocket updates during processing
5. **Advanced analytics** - Trend charts, comparisons
6. **User management** - Teams, permissions
7. **API rate limiting** - Protect backend
8. **Caching** - Redis for faster repeated queries

---

**Built with ❤️ as a clean, production-ready MVP**
