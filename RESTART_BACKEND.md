# 🔄 How to Restart Backend with New Code

## Quick Steps

### Windows (PowerShell)

1. **Stop the running backend**:
   - Press `Ctrl+C` in the terminal running the backend
   - Or close the terminal window

2. **Navigate to backend directory**:
   ```powershell
   cd backend
   ```

3. **Start the backend**:
   ```powershell
   python main.py
   ```

4. **Wait for models to load** (~30 seconds):
   ```
   🔧 Loading models globally...
   ✅ Whisper (medium) loaded
   ✅ Hindi→English translator loaded
   ✅ Groq LLM client initialized
   🎉 All models loaded successfully!
   ```

5. **Verify it's running**:
   - You should see: `Uvicorn running on http://0.0.0.0:8000`
   - Test: Open http://localhost:8000/health in browser

### Linux/Mac (Bash)

1. **Stop the running backend**:
   ```bash
   # Find the process
   ps aux | grep "python main.py"
   
   # Kill it
   kill <PID>
   ```

2. **Navigate and start**:
   ```bash
   cd backend
   python main.py
   ```

## Verify Groq Whisper is Active

After restarting, when you analyze files, you should see:

```
🔄 Processing: complaint_01.mp3
  🎤 Transcribing...
  ⚡ Using Groq Whisper API...        ← This means Groq is active!
  ✅ Groq transcription: 4.2s         ← Fast!
  ✅ Transcribed in 4.2s using groq
```

If you see this instead, Groq failed and it's using fallback:
```
  ⚡ Using Groq Whisper API...
  ⚠️ Groq failed: <error message>
  🔁 Falling back to local Whisper...
  ✅ Local transcription: 52.3s       ← Slower
```

## Troubleshooting

### Backend won't start

**Check Python version**:
```bash
python --version  # Should be 3.10+
```

**Check dependencies**:
```bash
pip install -r requirements.txt
```

**Check .env file**:
```bash
# Make sure these are set:
GROQ_API_KEY=your_key_here
MONGO_URI=your_mongodb_uri
```

### Groq API not working

**Check API key**:
- Open `.env` file
- Verify `GROQ_API_KEY` is set correctly
- Get a new key from https://console.groq.com/ if needed

**Check internet connection**:
- Groq API requires internet
- If offline, system will use local Whisper fallback

### Port 8000 already in use

**Windows**:
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill it (replace PID with actual number)
taskkill /PID <PID> /F
```

**Linux/Mac**:
```bash
# Find and kill process
lsof -ti:8000 | xargs kill -9
```

## Quick Restart Script

### Windows (restart_backend.bat)
```batch
@echo off
echo Stopping backend...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *main.py*" 2>nul
timeout /t 2 /nobreak >nul

echo Starting backend...
cd backend
start "SARCIS Backend" python main.py
echo Backend starting... Check the new window!
```

### Linux/Mac (restart_backend.sh)
```bash
#!/bin/bash
echo "Stopping backend..."
pkill -f "python main.py"
sleep 2

echo "Starting backend..."
cd backend
python main.py
```

Make executable:
```bash
chmod +x restart_backend.sh
```

## After Restart

1. **Frontend should reconnect automatically**
2. **Upload new files or re-analyze existing ones**
3. **Watch console for Groq Whisper messages**
4. **Enjoy 10-20x faster processing!** 🚀

## Need Help?

- Check logs in the backend terminal
- Verify all environment variables are set
- Ensure MongoDB is accessible
- Test Groq API key at https://console.groq.com/
