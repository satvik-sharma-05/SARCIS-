# Hybrid Analysis Setup Guide

## Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install groq==0.4.1
```

Or install all:
```bash
pip install -r requirements.txt
```

### 2. Get Groq API Key

1. Go to https://console.groq.com/
2. Sign up (free tier available)
3. Create an API key
4. Copy the key

### 3. Configure Environment

Edit `backend/.env`:
```env
GROQ_API_KEY=gsk_your_actual_api_key_here
```

### 4. Restart Backend

```bash
cd backend
python main.py
```

Look for:
```
✅ Groq LLM client initialized
```

### 5. Test

Upload audio and run analysis. Check logs for:
```
✨ Using LLM analysis          # LLM working!
⏱️ LLM timeout, using NLP      # Fallback working!
```

## Without Groq (NLP Only)

If you don't want to use Groq:

1. Don't add `GROQ_API_KEY` to `.env`
2. Or set it to: `GROQ_API_KEY=disabled`

System will use NLP only:
```
⚠️ Groq API key not configured, using NLP only
```

## Verification

### Check Logs

**With Groq**:
```
🔧 Initializing worker process...
✅ Whisper (small) loaded in worker
✅ Sentiment analyzer loaded in worker
✅ Hindi translator loaded in worker
✅ Groq LLM client initialized  ← Should see this
```

**Without Groq**:
```
🔧 Initializing worker process...
✅ Whisper (small) loaded in worker
✅ Sentiment analyzer loaded in worker
✅ Hindi translator loaded in worker
⚠️ Groq API key not configured, using NLP only  ← Expected
```

### Check Analysis

Look for `analysis_source` in results:
```json
{
  "text": "...",
  "events": [...],
  "sentiment": "...",
  "analysis_source": "llm"  // or "nlp"
}
```

## Performance

### With Groq
- First segment: ~1-2s (LLM call)
- Subsequent: ~50ms-2s (depends on LLM speed)
- Better accuracy

### Without Groq
- All segments: ~50ms (NLP only)
- Faster processing
- Good accuracy

## Troubleshooting

### "Groq API key not configured"
- Add key to `.env`
- Restart backend

### "LLM always times out"
- Check internet connection
- Increase timeout in code
- Check Groq status

### "Invalid API key"
- Verify key in Groq console
- Check for typos in `.env`
- Regenerate key if needed

### "Rate limit exceeded"
- Wait a few minutes
- Upgrade Groq plan
- Reduce timeout to skip more

## Cost Management

### Free Tier
- Groq offers generous free tier
- Sufficient for testing and small projects

### Optimization Tips
1. Increase skip threshold (20+ chars)
2. Reduce timeout (1 second)
3. Process fewer files at once
4. Use NLP only for non-critical clusters

## Summary

- ✅ Install: `pip install groq`
- ✅ Get key: https://console.groq.com/
- ✅ Add to `.env`: `GROQ_API_KEY=...`
- ✅ Restart backend
- ✅ Test and verify

System works with or without Groq!
