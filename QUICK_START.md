# 🚀 Quick Start - Optimized Pipeline

## Install & Run (3 Commands)

```bash
# 1. Install new dependency
cd backend
pip install sacremoses==0.1.1

# 2. Start backend (models load automatically)
python main.py

# 3. Start frontend (in new terminal)
cd frontend
npm run dev
```

## What You'll See

### Backend Startup:
```
🔧 Loading models globally...
✅ Whisper (medium) loaded
✅ Hindi→English translator loaded
✅ Groq LLM client initialized
🎉 All models loaded successfully!
```

### During Processing:
```
🔄 Processing: complaint_01.mp3
  🎤 Transcribing...
  ✅ Transcribed in 45.23s (12 segments)
  🌐 Translating full transcript...
  ✅ Translated in 1.45s
  ✨ Analyzing with LLM...
  ✅ LLM analysis in 2.31s
  ✅ Completed in 49.12s
```

## Performance

- **Before**: 5-7 minutes per file ❌
- **Now**: 1-2 minutes per file ✅
- **Improvement**: 3-5x faster 🚀

## Test Files Available

```
backend/uploads/69e29c20b890f00e353a80ee/
  ├── complaint_01.mp3
  ├── help.mp3
  ├── threat_01.mp3
  └── threat_02.mp3
```

Use cluster ID: `69e29c20b890f00e353a80ee` to re-analyze these files.

## Key Features

✅ Whisper medium model (high accuracy)  
✅ Hindi/English/Hinglish translation  
✅ LLM-powered intelligence (70B model)  
✅ Rich contextual insights  
✅ 3-5x faster processing  
✅ Clean output (no warnings)  

## Need Help?

See `OPTIMIZATION_COMPLETE.md` for full details and troubleshooting.
