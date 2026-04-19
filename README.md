# SARCIS - Smart Audio Risk & Context Intelligence System

🧠 **Cluster-based Audio Intelligence Platform with Parallel Processing**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14-black.svg)](https://nextjs.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green.svg)](https://www.mongodb.com/)

---

## 🚀 What It Does

Upload audio files → Organize into clusters → Process in parallel → Extract multi-layered insights → Interactive results

### Key Features
- 🔐 **Authentication** - Secure signup/login
- 📁 **Cluster Management** - Organize audio files into projects
- 📤 **Multi-file Upload** - Drag & drop .wav, .mp3, .m4a
- ⚡ **Parallel Processing** - 4 workers processing simultaneously
- 🧠 **Multi-layered AI Insights**:
  - Events (complaint, urgency, escalation, etc.)
  - Sentiment (positive/negative/neutral)
  - Intent (refund_request, technical_issue, etc.)
  - Priority (critical/high/medium/low)
  - Risk Signals (legal_threat, fraud_allegation, etc.)
  - Keywords extraction
  - Confidence scores
- 📊 **Cluster Analytics** - Aggregated insights across all files
- 🎧 **Audio Playback** - Click segment → jump to timestamp
- 📈 **Interactive Dashboard** - Visual insights and trends

---

## 🧩 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Next.js 14, Tailwind CSS, Framer Motion, WaveSurfer.js |
| **Backend** | FastAPI, Python multiprocessing |
| **Database** | MongoDB (Motor async driver) |
| **AI/ML** | OpenAI Whisper, Hugging Face Transformers |
| **Storage** | Local filesystem (/uploads) |
| **Deployment** | Vercel (frontend), Render (backend), MongoDB Atlas |

---

## 📦 Installation

### Prerequisites
- Python 3.9+
- Node.js 18+
- MongoDB (local or Atlas)

### 1. Clone Repository
```bash
git clone <your-repo>
cd SARCIS
```

### 2. Backend Setup
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your MongoDB URI and JWT secret

# Run server
python main.py
```

Backend runs on: **http://localhost:8000**

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Create .env.local
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Run development server
npm run dev
```

Frontend runs on: **http://localhost:3000**

---

## 🔧 Environment Variables

### Backend (.env)
```env
MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/
MONGODB_DB_NAME=sarcis
JWT_SECRET_KEY=your-secret-key-change-in-production
WHISPER_MODEL=base
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 🎯 Usage Flow

1. **Sign up / Login** at http://localhost:3000
2. **Create a cluster** (e.g., "Customer Calls")
3. **Upload audio files** (drag & drop)
4. **Click "Run Analysis"** - processes in parallel
5. **View results** with:
   - Timestamp-level insights
   - Cluster analytics dashboard
   - Interactive audio playback

---

## 🏗️ Architecture

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

See [ARCHITECTURE.md](./ARCHITECTURE.md) for detailed system design.

---

## 📊 Insights Layers

### Per Segment
```json
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
```

### Per File
```json
{
  "total_segments": 45,
  "negative_percentage": 60.5,
  "high_priority_count": 12,
  "top_issue": "complaint",
  "overall_sentiment": "negative"
}
```

### Per Cluster
```json
{
  "total_files": 100,
  "total_segments": 4500,
  "complaint_percentage": 45.2,
  "urgency_percentage": 23.1,
  "negative_percentage": 38.7,
  "high_priority_percentage": 15.3
}
```

---

## ⚡ Performance

| Files | Processing Time |
|-------|----------------|
| 50    | 5-10 minutes   |
| 100   | 10-20 minutes  |
| 500   | ~1 hour        |

**Optimization:**
- 4 parallel workers (multiprocessing)
- Efficient Whisper base model
- Batch database operations
- Async I/O operations

---

## 🔌 API Endpoints

### Authentication
```
POST   /auth/signup
POST   /auth/login
```

### Clusters
```
GET    /clusters
POST   /clusters
DELETE /clusters/{id}
GET    /clusters/{id}/files
GET    /clusters/{id}/insights
```

### Files
```
POST   /upload
```

### Analysis
```
POST   /analyze/{cluster_id}
GET    /results/{cluster_id}
```

---

## 📁 Project Structure

```
backend/
├── main.py              # FastAPI app
├── db.py                # MongoDB connection
├── models.py            # Data models
├── services/
│   ├── auth.py          # Authentication
│   └── processor.py     # Audio processing (multiprocessing)
├── uploads/             # Audio files storage
└── requirements.txt

frontend/
├── app/
│   ├── page.tsx         # Home
│   ├── login/           # Login page
│   ├── signup/          # Signup page
│   ├── dashboard/       # Clusters list
│   ├── cluster/[id]/    # Cluster detail + upload
│   └── results/[id]/    # Analysis results + insights
├── lib/
│   └── api.ts           # API client
└── package.json
```

---

## 🚀 Deployment

### Frontend (Vercel)
```bash
cd frontend
vercel deploy
```

### Backend (Render)
1. Create new Web Service
2. Connect GitHub repo
3. Build command: `pip install -r requirements.txt`
4. Start command: `python main.py`
5. Add environment variables

### Database (MongoDB Atlas)
1. Create free cluster
2. Get connection string
3. Add to backend .env

---

## 🎓 Interview Talking Points

### One-Liner
> "A cluster-based audio intelligence platform that uses Python multiprocessing to parallelize audio analysis, extracting multi-layered insights including sentiment, intent, events, and risk signals—all without requiring distributed infrastructure."

### Technical Highlights
- **Parallel Processing**: 4 workers using Python multiprocessing
- **Multi-layered Insights**: 8 layers of analysis per segment
- **Scalable Design**: Handles 100s of files efficiently
- **Clean Architecture**: No Redis, Celery, or Docker complexity
- **Production-Ready**: Complete user flow with authentication

### Architecture Decisions
- **Why multiprocessing?** - Fast, simple, no external dependencies
- **Why MongoDB?** - Flexible schema for varying insights
- **Why FastAPI?** - High performance, async support, auto docs
- **Why Next.js?** - SSR, great DX, easy deployment

---

## ⚠️ Limitations

### What This System IS
✅ Fast parallel processing (4-6 files at once)
✅ Multi-layered AI insights
✅ Scalable to hundreds of files
✅ Production-ready MVP
✅ Free to run locally

### What This System IS NOT
❌ Distributed system (no Kubernetes)
❌ Real-time streaming
❌ Infinite scalability (CPU-bound)
❌ Cloud-native (single server)

---

## 📚 Documentation

- [ARCHITECTURE.md](./ARCHITECTURE.md) - Detailed system design
- [API Docs](http://localhost:8000/docs) - Interactive API documentation (when running)

---

## 🤝 Contributing

This is a portfolio/learning project. Feel free to fork and customize!

---

## 📄 License

MIT License - See LICENSE file

---

## 🎯 What You Built

✅ **AI system** - Real ML/NLP pipeline
✅ **Scalable design** - Parallel processing
✅ **Production workflow** - Complete user flow
✅ **Multi-layered insights** - Not just "threat detection"
✅ **Interview-ready** - Can explain architecture clearly

---

**Built with ❤️ as a clean, production-ready MVP**

For questions or feedback, open an issue!
