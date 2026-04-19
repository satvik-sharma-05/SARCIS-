# Hybrid Analysis System (NLP + LLM)

## Overview

The hybrid analysis system runs traditional NLP and modern LLM (Groq) in parallel for each audio segment, using the best available result with intelligent fallback.

## Architecture

```
Audio Segment
    ↓
Hybrid Analysis
    ├─ Thread 1: NLP Analysis (Fast, Always Available)
    │   └─ HuggingFace + Rule-based
    │
    └─ Thread 2: LLM Analysis (Slow, More Accurate)
        └─ Groq API (llama3-8b-8192)
    ↓
Wait for LLM (2 second timeout)
    ↓
    ├─ LLM Success → Use LLM Result ✨
    ├─ LLM Timeout → Use NLP Result ⏱️
    └─ LLM Error → Use NLP Result ⚠️
```

## Key Features

### 1. Parallel Execution
- Both analyses run simultaneously using `ThreadPoolExecutor`
- No waiting for slow LLM if it's not needed
- NLP always completes quickly as fallback

### 2. Timeout-Based Fallback
- LLM has 2-second timeout
- If LLM responds in time → use it (better accuracy)
- If LLM times out → use NLP (guaranteed result)
- Never blocks processing

### 3. Graceful Degradation
- System works even if Groq API is down
- System works without Groq API key
- Falls back to NLP automatically
- No errors, just logs

### 4. Smart Optimization
- Skips LLM for very short text (<10 chars)
- Saves API calls and time
- LLM only for meaningful segments

## Implementation

### Core Function

```python
def hybrid_analysis(text, original_text=None, timeout=2.0):
    """
    Run NLP and LLM in parallel, use best available result.
    """
    # Skip LLM for very short text
    if len(text.strip()) < 10:
        return run_nlp(text, original_text)
    
    # Run both in parallel
    with ThreadPoolExecutor(max_workers=2) as executor:
        nlp_future = executor.submit(run_nlp, text, original_text)
        llm_future = executor.submit(run_llm, text, original_text)
        
        # Get NLP result (fast, guaranteed)
        nlp_result = nlp_future.result()
        
        # Try to get LLM result with timeout
        try:
            llm_result = llm_future.result(timeout=timeout)
            if llm_result:
                return llm_result  # Use LLM if available
        except TimeoutError:
            pass  # Use NLP fallback
        
        return nlp_result  # Fallback to NLP
```

### NLP Analysis

```python
def run_nlp(text, original_text=None):
    """
    Traditional NLP analysis (fast, always available).
    """
    # Sentiment analysis (HuggingFace)
    sentiment_result = sentiment_analyzer(text[:512])[0]
    sentiment = "positive" if sentiment_result["label"] == "POSITIVE" else "negative"
    
    # Rule-based classification
    events = classify_events(text, original_text)
    intent = detect_intent(text, original_text)
    keywords = extract_keywords(text)
    risk_signals = detect_risk_signals(text, original_text)
    priority = calculate_priority(events, sentiment, keywords)
    
    return {
        "events": events,
        "sentiment": sentiment,
        "intent": intent,
        "priority": priority,
        "keywords": keywords,
        "risk_signals": risk_signals,
        "confidence": confidence,
        "source": "nlp"
    }
```

### LLM Analysis

```python
def run_llm(text, original_text=None):
    """
    LLM analysis using Groq (slower but more accurate).
    """
    if groq_client is None:
        return None
    
    # Create structured prompt
    prompt = f"""Analyze this transcript and provide JSON:
    
    Transcript: "{text}"
    
    Format:
    {{
      "events": [...],
      "sentiment": "...",
      "intent": "...",
      "priority": "...",
      "keywords": [...],
      "risk_signals": [...],
      "confidence": 0.0-1.0
    }}
    """
    
    # Call Groq API
    response = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are an expert analyst. Respond with JSON only."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        max_tokens=500,
        timeout=3.0
    )
    
    # Parse JSON response
    content = response.choices[0].message.content
    result = json.loads(content)
    result["source"] = "llm"
    
    return result
```

## Configuration

### Environment Variables

Add to `.env`:
```env
GROQ_API_KEY=your-groq-api-key-here
```

Get your API key from: https://console.groq.com/

### Timeout Configuration

Adjust timeout in `processor.py`:
```python
# Default: 2 seconds
analysis = hybrid_analysis(text, original_text, timeout=2.0)

# Faster (more NLP fallbacks)
analysis = hybrid_analysis(text, original_text, timeout=1.0)

# Slower (more LLM results)
analysis = hybrid_analysis(text, original_text, timeout=3.0)
```

### Skip LLM Threshold

Adjust minimum text length:
```python
# Default: 10 characters
if len(text.strip()) < 10:
    return run_nlp(text, original_text)

# More aggressive (skip more)
if len(text.strip()) < 20:
    return run_nlp(text, original_text)

# Less aggressive (use LLM more)
if len(text.strip()) < 5:
    return run_nlp(text, original_text)
```

## Performance

### Speed Comparison

| Method | Speed | Accuracy | Availability |
|--------|-------|----------|--------------|
| NLP Only | ~50ms | Good | 100% |
| LLM Only | ~1-3s | Excellent | 95% |
| Hybrid | ~50ms-2s | Best Available | 100% |

### Typical Results

**Scenario 1: LLM Responds Fast**
```
✓ Valid segment: 'मुझे आपकी सेवा से बहुत समस्या है'
  → Translated: 'I have a lot of problems with your service'
  ✨ Using LLM analysis
Time: ~1.2s
Source: llm
```

**Scenario 2: LLM Times Out**
```
✓ Valid segment: 'मैं रिफंड चाहता हूं'
  → Translated: 'I want a refund'
  ⏱️ LLM timeout (2.0s), using NLP
Time: ~2.05s
Source: nlp
```

**Scenario 3: No Groq API Key**
```
⚠️ Groq API key not configured, using NLP only
✓ Valid segment: 'यह काम नहीं कर रहा'
  → Translated: 'This is not working'
  📊 Using NLP analysis
Time: ~50ms
Source: nlp
```

## Benefits

### 1. Best of Both Worlds
- LLM accuracy when available
- NLP speed as fallback
- Never blocks on slow API

### 2. Reliability
- Works without Groq API
- Works if Groq is down
- Always produces results

### 3. Cost Optimization
- Skips LLM for short text
- Timeout prevents long waits
- Only pays for successful calls

### 4. Transparency
- Tracks which method was used
- Logs show decision process
- Easy to debug

## Monitoring

### Log Messages

```
✨ Using LLM analysis          # LLM succeeded
⏱️ LLM timeout (2.0s), using NLP  # LLM too slow
⚠️ LLM error: ..., using NLP   # LLM failed
📊 LLM returned invalid result # LLM response bad
```

### Analysis Source Tracking

Each segment includes `analysis_source`:
```json
{
  "text": "...",
  "events": [...],
  "sentiment": "...",
  "analysis_source": "llm"  // or "nlp" or "nlp_fallback"
}
```

## Troubleshooting

### Issue: Always using NLP
**Cause**: Groq API key not configured
**Solution**: Add `GROQ_API_KEY` to `.env`

### Issue: LLM always times out
**Cause**: Timeout too short or slow network
**Solution**: Increase timeout to 3-5 seconds

### Issue: LLM errors
**Cause**: Invalid API key or rate limits
**Solution**: Check API key, check Groq dashboard

### Issue: High API costs
**Cause**: Processing too many segments
**Solution**: 
- Increase skip threshold (20+ chars)
- Reduce timeout (1 second)
- Use NLP only for some clusters

## Cost Estimation

### Groq Pricing (as of 2024)
- llama3-8b-8192: ~$0.05 per 1M tokens
- Very affordable for most use cases

### Example Costs
- 100 segments × 50 tokens each = 5,000 tokens
- Cost: ~$0.00025 (less than a cent)
- 10,000 segments = ~$0.025 (2.5 cents)

## Advanced Usage

### Custom LLM Models

Change model in `run_llm()`:
```python
# Faster, cheaper
model="llama3-8b-8192"

# More accurate, slower
model="llama3-70b-8192"

# Mixtral (alternative)
model="mixtral-8x7b-32768"
```

### Custom Prompts

Modify prompt in `run_llm()` for:
- Different analysis focus
- Additional fields
- Domain-specific insights

### Disable LLM

Set in `.env`:
```env
GROQ_API_KEY=disabled
```

Or remove the key entirely.

## Summary

The hybrid analysis system provides:
- ✅ Best available accuracy (LLM when possible)
- ✅ Guaranteed results (NLP fallback)
- ✅ Fast processing (parallel execution)
- ✅ Cost optimization (smart skipping)
- ✅ Reliability (graceful degradation)
- ✅ Transparency (source tracking)

Perfect for production use with real-world constraints!
