# 🚀 Quick Start - Phase 1

## Installation (5 minutes)

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Generate JWT Secret
```bash
# Linux/Mac
openssl rand -hex 32

# Windows PowerShell
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output and update `.env`:
```env
JWT_SECRET_KEY=paste_your_generated_key_here
```

### 3. Start MongoDB (if not running)
```bash
# Using Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest

# Or use your existing MongoDB Atlas (already in .env)
```

### 4. Start Backend
```bash
cd backend
python main.py
```

✅ Backend running on `http://localhost:8000`

## Test It (2 minutes)

### Option 1: Automated Test
```bash
python test_phase1.py
```

### Option 2: Manual Test (Swagger UI)
1. Open `http://localhost:8000/docs`
2. Click `/api/auth/signup`
3. Click "Try it out"
4. Fill in:
   ```json
   {
     "email": "test@example.com",
     "password": "Test123!",
     "name": "Test User"
   }
   ```
5. Click "Execute"
6. Copy the `access_token`
7. Click "Authorize" button (top right)
8. Paste token
9. Now test other endpoints!

## Quick API Reference

### Authentication
```bash
# Signup
POST /api/auth/signup
Body: { "email": "...", "password": "...", "name": "..." }

# Login
POST /api/auth/login
Body: { "email": "...", "password": "..." }

# Get Profile
GET /api/auth/me
Header: Authorization: Bearer TOKEN
```

### Clusters
```bash
# Create
POST /api/clusters
Header: Authorization: Bearer TOKEN
Body: { "name": "...", "description": "..." }

# List
GET /api/clusters
Header: Authorization: Bearer TOKEN

# Get Details
GET /api/clusters/{id}
Header: Authorization: Bearer TOKEN
```

### Files
```bash
# Upload
POST /api/clusters/{id}/upload
Header: Authorization: Bearer TOKEN
Body: files (multipart/form-data)

# List
GET /api/clusters/{id}/files
Header: Authorization: Bearer TOKEN
```

## What You Can Do Now

✅ Create user accounts  
✅ Login with JWT authentication  
✅ Create clusters (organize audio files)  
✅ Upload audio files to clusters  
✅ List and manage clusters  
✅ Delete files and clusters  

## What's Coming in Phase 2

⏳ Process audio files (Whisper + NLP + GenAI)  
⏳ Job queue for background processing  
⏳ Progress tracking  
⏳ View analysis results  
⏳ Cluster analytics  

## File Structure

```
backend/
├── auth/              ← JWT & password handling
├── database/          ← MongoDB models & repos
├── routes/            ← API endpoints
├── uploads/           ← Uploaded files (auto-created)
├── main.py            ← FastAPI app
└── requirements.txt   ← Dependencies
```

## Troubleshooting

**Backend won't start?**
```bash
pip install -r requirements.txt
```

**MongoDB connection error?**
- Check `MONGO_URI` in `.env`
- Or start local MongoDB

**JWT token invalid?**
- Generate new secret key
- Update `JWT_SECRET_KEY` in `.env`

**Can't upload files?**
- Only audio files: `.wav`, `.mp3`, `.m4a`, `.flac`, `.ogg`
- Max size: 100MB per file

## Need Help?

1. Check `PHASE1_SETUP.md` for detailed setup
2. Check `PHASE1_COMPLETE.md` for architecture
3. Check `API_SPEC.md` for full API docs
4. Open `http://localhost:8000/docs` for interactive docs

---

**Phase 1 Complete!** Ready for Phase 2? 🚀
