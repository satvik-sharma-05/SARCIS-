# 🚀 Quick Start Guide

Get SARCIS running in 5 minutes!

## Prerequisites Check

```bash
# Check Python version (need 3.9+)
python --version

# Check Node.js version (need 18+)
node --version

# Check if MongoDB is accessible (or use Atlas)
```

## Step 1: Clone & Setup (2 min)

```bash
# Clone repository
git clone <your-repo>
cd SARCIS

# Backend setup
cd backend
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install
```

## Step 2: Configure Environment (1 min)

### Backend (.env)
```bash
cd backend
cat > .env << EOF
MONGO_URI=mongodb+srv://satvik:123@cluster0.qyfpiti.mongodb.net/?appName=Cluster0
MONGODB_DB_NAME=sarcis
JWT_SECRET_KEY=your-secret-key-change-in-production
WHISPER_MODEL=base
EOF
```

### Frontend (.env.local)
```bash
cd frontend
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

## Step 3: Start Services (2 min)

### Option A: Using start script (Windows)
```bash
# From project root
start.bat
```

### Option B: Manual start

**Terminal 1 - Backend:**
```bash
cd backend
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## Step 4: Use the System! 🎉

1. Open http://localhost:3000
2. Sign up with email/password
3. Create a cluster (e.g., "Test Calls")
4. Upload audio files (.wav, .mp3, .m4a)
5. Click "Run Analysis"
6. View results with insights!

---

## 🎯 Test with Sample Audio

Don't have audio files? Use these:

1. Record a voice memo on your phone
2. Use text-to-speech tools
3. Download sample audio from:
   - https://freesound.org/
   - https://www.zapsplat.com/

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill process if needed
taskkill /PID <process_id> /F
```

### Frontend won't start
```bash
# Check if port 3000 is in use
netstat -ano | findstr :3000

# Kill process if needed
taskkill /PID <process_id> /F
```

### Models taking too long to load
- First run downloads Whisper model (~140MB)
- Subsequent runs are faster
- Use `WHISPER_MODEL=tiny` for faster loading (less accurate)

### MongoDB connection error
- Check MONGO_URI in .env
- Ensure MongoDB Atlas IP whitelist includes your IP
- Or use local MongoDB: `MONGO_URI=mongodb://localhost:27017`

---

## 📊 Expected Performance

| Action | Time |
|--------|------|
| First startup | 30-60 seconds (model loading) |
| Subsequent startups | 5-10 seconds |
| Upload 10 files | 2-5 seconds |
| Process 10 files | 2-5 minutes |
| Process 50 files | 5-10 minutes |

---

## 🎓 Next Steps

1. Read [ARCHITECTURE.md](./ARCHITECTURE.md) for system design
2. Check [README.md](./README.md) for full documentation
3. Explore API docs at http://localhost:8000/docs
4. Customize insights in `backend/services/processor.py`

---

**You're all set! 🚀**
