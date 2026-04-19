# SARCIS - Technical Tutorial & Learning Guide

> Complete technical breakdown for learning, interviews, and deep understanding

## 📚 Table of Contents

1. [Project Overview](#1-project-overview)
2. [File Structure](#2-file-structure-explained)
3. [Complete Pipeline Flow](#3-complete-pipeline-flow)
4. [Request Flow](#4-request-flow-api-to-response)
5. [Key Functions](#5-key-functions-explained)
6. [Design Decisions](#6-key-design-decisions)
7. [Data Transformations](#7-data-flow--transformations)
8. [Interview Prep](#8-interview-preparation-qa)

---

## 1. Project Overview

### Problem Statement
Customer service teams receive thousands of audio recordings but:
- Manual analysis takes hours per file
- Inconsistent human evaluation
- Can't scale to handle volume
- Miss patterns across recordings

### Solution
Automated AI pipeline:
- Transcribes audio in 3-10 seconds
- Translates multilingual content
- Extracts insights using 70B LLM
- Interactive dashboard for analysis

### Tech Stack
- **Backend**: FastAPI + Python + MongoDB
- **Frontend**: Next.js 14 + TypeScript + Tailwind
- **AI**: Groq (Whisper + Llama 3.3 70B), Helsinki NLP
- **Auth**: JWT + bcrypt

---

## 2. File Structure Explained

### Backend (`backend/`)

**`main.py`** - FastAPI application with all HTTP endpoints
- Auth routes: `/auth/signup`, `/auth/login`
- Cluster routes: `/clusters` (CRUD operations)
- File routes: `/upload`, `/clusters/{id}/files`
- Analysis routes: `/analyze/{id}`, `/reanalyze/{id}`
- Results routes: `/results/{id}`, `/clusters/{id}/insights`
- Audio serving: `/audio/{cluster_id}/{file_name}`

**`db.py`** - MongoDB connection management
- `get_db()`: Returns database instance
- `init_db()`: Initializes connection on startup

**`models.py`** - Pydantic data models
- `User`, `Cluster`, `FileRecord`, `Result`
- Used for validation and type safety

**`services/auth.py`** - Authentication logic
- `hash_password()`: Bcrypt password hashing
- `verify_password()`: Password verification
- `create_access_token()`: JWT token generation
- `verify_token()`: JWT token validation

**`services/processor.py`** - Audio processing pipeline (CORE)
- `transcribe_with_groq()`: Groq Whisper API transcription
- `transcribe_local()`: Local Whisper fallback
- `transcribe()`: Smart router with fallback
- `translate_full_text()`: Hindi→English translation
- `analyze_with_llm()`: LLM intelligence extraction
- `create_segments_from_whisper()`: Segment creation
- `process_single_file()`: Main file processing
- `process_cluster()`: Batch file processing
- `calculate_cluster_insights()`: Aggregated analytics

### Frontend (`frontend/`)

**`app/layout.tsx`** - Root layout with global styles

**`app/page.tsx`** - Landing page

**`app/login/page.tsx`** - Login page with form

**`app/signup/page.tsx`** - Signup page with form

**`app/dashboard/page.tsx`** - Main dashboard showing clusters

**`app/cluster/[id]/page.tsx`** - Cluster details with file list

**`app/results/[id]/page.tsx`** - Analysis results with insights

**`lib/api.ts`** - API client with axios
- `auth.signup()`, `auth.login()`
- `clusters.list()`, `clusters.create()`, `clusters.delete()`
- `files.upload()`, `files.list()`
- `analysis.analyze()`, `analysis.results()`, `analysis.insights()`

**`lib/auth-context.tsx`** - React context for authentication
- Manages user state and token
- Provides login/logout functions

---

## 3. Complete Pipeline Flow

### Step-by-Step Processing

```
1. USER UPLOADS AUDIO
   ↓
   Frontend → POST /upload → Backend
   ↓
   Save file to: backend/uploads/{cluster_id}/{filename}
   Store metadata in MongoDB: files collection

2. USER CLICKS "ANALYZE"
   ↓
   Frontend → POST /analyze/{cluster_id} → Backend
   ↓
   Get unprocessed files from MongoDB
   ↓
   For each file:

3. TRANSCRIPTION (Fast)
   ↓
   Try: Groq Whisper API (3-10 seconds)
   ├─ Success → Continue
   └─ Fail → Local Whisper (40-90 seconds)
   ↓
   Output: Full transcript + segments with timestamps

4. TRANSLATION (If needed)
   ↓
   Detect language (Hindi/English/Hinglish)
   ↓
   If not English:
      Helsinki NLP model translates full transcript
   ↓
   Output: English text for LLM analysis

5. LLM ANALYSIS (Once per file)
   ↓
   Send full transcript to Groq Llama 3.3 70B
   ↓
   Extract:
   - Overall sentiment (type + intensity)
   - Primary intent
   - Risk level (low/moderate/high/extreme)
   - Urgency (low/medium/high/immediate)
   - Key events (complaint, threat, etc.)
   - Entities (names, products, amounts)
   - Summary
   ↓
   Output: File-level intelligence JSON

6. SEGMENT CREATION
   ↓
   For each Whisper segment:
      Inherit file-level intelligence
      Add timestamp and text
   ↓
   Output: Array of enriched segments

7. SAVE TO DATABASE
   ↓
   Store in MongoDB: results collection
   {
      cluster_id,
      file_id,
      file_name,
      segments: [...],
      summary: {...},
      language
   }

8. CALCULATE CLUSTER INSIGHTS
   ↓
   Aggregate across all files:
   - Total files/segments
   - Sentiment distribution
   - Event counts
   - Priority distribution
   - Top issues
   - File rankings
   ↓
   Store in: cluster_insights collection

9. RETURN TO FRONTEND
   ↓
   Frontend fetches:
   - GET /results/{cluster_id} → All file results
   - GET /clusters/{cluster_id}/insights → Aggregated insights
   ↓
   Display in interactive dashboard
```

---

## 4. Request Flow (API to Response)

### Example: Analyzing Audio Files

**1. Frontend Request**
```typescript
// User clicks "Analyze" button
const response = await api.post(`/analyze/${clusterId}`);
```

**2. Backend Receives Request**
```python
@app.post("/analyze/{cluster_id}")
async def analyze_cluster(cluster_id: str, user = Depends(get_current_user)):
    # Verify user owns cluster
    # Get unprocessed files
    # Call process_cluster()
```

**3. Process Cluster**
```python
async def process_cluster(cluster_id: str, files: List[dict]):
    # For each file sequentially:
    for file in files:
        result = process_single_file(file, cluster_id)
        # Save result to database
```

**4. Process Single File**
```python
def process_single_file(file_record: dict, cluster_id: str):
    # 1. Transcribe (Groq or local)
    result, method, time = transcribe(file_path)
    
    # 2. Translate if needed
    translated = translate_full_text(transcript, language)
    
    # 3. LLM analysis
    intelligence = analyze_with_llm(translated or transcript)
    
    # 4. Create segments
    segments = create_segments_from_whisper(result, intelligence)
    
    # 5. Return result
    return {file_id, segments, summary, ...}
```

**5. Database Storage**
```python
# Save to MongoDB
await db.results.insert_one({
    "cluster_id": cluster_id,
    "file_id": file_id,
    "segments": segments,
    ...
})
```

**6. Frontend Receives Response**
```typescript
// Response: {message: "Analysis completed", files_processed: 4}
// Frontend then fetches results
const results = await api.get(`/results/${clusterId}`);
const insights = await api.get(`/clusters/${clusterId}/insights`);
```

**7. Display in UI**
```typescript
// Show insights dashboard
// List files with summaries
// Allow audio playback with segment navigation
```

---

## 5. Key Functions Explained

### Transcription Functions

**`transcribe_with_groq(audio_path)`**
- Opens audio file in binary mode
- Calls Groq Whisper API with whisper-large-v3
- Returns: `{text, language, segments}`
- Fast: 3-10 seconds per file

**`transcribe_local(audio_path)`**
- Uses local OpenAI Whisper medium model
- Thread-locked for safety (PyTorch not thread-safe)
- Returns: `{text, language, segments}`
- Slower: 40-90 seconds per file

**`transcribe(audio_path)`**
- Smart router: tries Groq first, falls back to local
- Returns: `(result, method, time)`
- Ensures 100% reliability

### Translation Function

**`translate_full_text(text, source_lang)`**
- Uses Helsinki NLP MarianMT model
- Translates Hindi/Urdu to English
- Chunks long text (max 400 words per chunk)
- Returns: English translation or None

### LLM Analysis Function

**`analyze_with_llm(text, original_text)`**
- Sends full transcript to Groq Llama 3.3 70B
- Prompt asks for structured JSON output
- Extracts: sentiment, intent, risk, urgency, events, entities, summary
- Returns: Intelligence dict or None on failure

### Segment Creation Function

**`create_segments_from_whisper(whisper_result, file_level_analysis)`**
- Takes Whisper segments + file-level intelligence
- Each segment inherits file-level insights
- Adds: start/end time, text, language
- Returns: Array of enriched segments

### Processing Functions

**`process_single_file(file_record, cluster_id)`**
- Main orchestrator for one file
- Calls: transcribe → translate → analyze → create segments
- Logs timing for each step
- Returns: Complete result dict

**`process_cluster(cluster_id, files)`**
- Processes all files sequentially
- Updates file status in database
- Calculates cluster insights
- Handles errors gracefully

---

## 6. Key Design Decisions

### Why Groq Whisper API?
- **Speed**: 10-20x faster than local (3-10s vs 40-90s)
- **Accuracy**: Uses whisper-large-v3 (better than medium)
- **Cost**: Free for reasonable usage
- **Scalability**: Cloud-based, no local compute needed

### Why Keep Local Whisper Fallback?
- **Reliability**: 100% uptime even if API fails
- **Offline**: Works without internet
- **Rate Limits**: Handles API quota issues
- **Redundancy**: No single point of failure

### Why Translate Once Per File?
- **Efficiency**: Faster than per-segment translation
- **Context**: Better translation with full context
- **Cost**: Fewer API calls
- **Simplicity**: Cleaner code

### Why LLM Analysis Once Per File?
- **Context**: Full conversation understanding
- **Efficiency**: One API call vs many
- **Consistency**: Same intelligence across segments
- **Cost**: Reduces API usage

### Why Sequential Processing?
- **Stability**: PyTorch models not thread-safe
- **Memory**: One model instance in memory
- **Predictability**: Linear processing time
- **Simplicity**: Easier to debug

### Why MongoDB?
- **Flexibility**: Schema-less for evolving data
- **Scalability**: Handles large volumes
- **JSON**: Native JSON storage (perfect for our data)
- **Aggregation**: Powerful analytics queries

### Why Next.js?
- **Performance**: Server-side rendering
- **Developer Experience**: Great tooling
- **TypeScript**: Type safety
- **App Router**: Modern routing system

---

## 7. Data Flow & Transformations

### Audio File → Transcript
```
Input: audio.mp3 (binary)
↓
Groq Whisper API / Local Whisper
↓
Output: {
  text: "full transcript...",
  language: "hi",
  segments: [
    {start: 0.0, end: 5.2, text: "..."},
    ...
  ]
}
```

### Transcript → Translation
```
Input: "मुझे मदद चाहिए..."
↓
Helsinki NLP MarianMT
↓
Output: "I need help..."
```

### Translation → LLM Intelligence
```
Input: "I need help with my order..."
↓
Groq Llama 3.3 70B
↓
Output: {
  overall_sentiment: {type: "frustrated", intensity: 0.7},
  primary_intent: "refund_request",
  risk_level: "moderate",
  urgency: "high",
  key_events: ["complaint", "refund_demand"],
  entities: ["order_number", "product_name"],
  summary: "Customer frustrated about delayed order..."
}
```

### Intelligence → Segments
```
Input: Whisper segments + File intelligence
↓
Merge and enrich
↓
Output: [
  {
    start: 0.0,
    end: 5.2,
    text: "...",
    sentiment: "frustrated",
    sentiment_intensity: 0.7,
    intent: "refund_request",
    priority: "high",
    risk_level: "moderate",
    events: ["complaint"],
    entities: ["order_123"],
    ...
  },
  ...
]
```

### Segments → Database
```
MongoDB Document:
{
  _id: ObjectId("..."),
  cluster_id: "69e4d879...",
  file_id: "69e4d880...",
  file_name: "complaint_01.mp3",
  segments: [...],
  summary: {
    total_segments: 12,
    negative_percentage: 75.0,
    high_priority_count: 8,
    top_issue: "refund_demand",
    overall_sentiment: "frustrated",
    language: "hi"
  },
  language: "hi"
}
```

---

## 8. Interview Preparation Q&A

### Architecture Questions

**Q: Explain the overall architecture**
A: Three-tier architecture:
- Frontend (Next.js) - User interface
- Backend (FastAPI) - API server and business logic
- Database (MongoDB) - Data persistence
- External APIs (Groq) - AI processing

**Q: How does the audio processing pipeline work?**
A: Sequential pipeline:
1. Transcribe (Groq Whisper API with local fallback)
2. Translate (Helsinki NLP if non-English)
3. Analyze (Groq Llama 3.3 70B for intelligence)
4. Create segments (inherit file-level insights)
5. Store results (MongoDB)
6. Calculate insights (aggregated analytics)

**Q: Why use Groq instead of OpenAI?**
A: 
- Faster inference (optimized hardware)
- Lower latency for real-time apps
- Cost-effective for our use case
- Supports both Whisper and Llama models

### Technical Questions

**Q: How do you handle API failures?**
A: Automatic fallback system:
- Try Groq Whisper first
- If fails, use local Whisper
- Ensures 100% reliability
- Logs which method was used

**Q: Why process files sequentially instead of parallel?**
A:
- PyTorch models (Whisper) not thread-safe
- Prevents memory issues
- More stable and predictable
- Still fast with Groq (5-15s per file)

**Q: How do you ensure data security?**
A:
- JWT authentication for API
- Bcrypt password hashing
- Environment variables for secrets
- MongoDB connection security
- User-based access control

**Q: How does the frontend communicate with backend?**
A:
- REST API over HTTP
- Axios for HTTP requests
- JWT token in Authorization header
- JSON data format
- CORS enabled for localhost

### Performance Questions

**Q: What's the processing speed?**
A:
- With Groq: 5-15 seconds per file
- With fallback: 45-95 seconds per file
- Transcription: 3-10s (Groq) or 40-90s (local)
- Translation: 1-2s
- LLM: 1-3s

**Q: How do you optimize for speed?**
A:
- Groq API for fast transcription
- Translate once per file (not per segment)
- LLM analysis once per file
- Load models once at startup
- Efficient database queries

**Q: Can it scale to thousands of files?**
A:
- Yes, sequential processing is stable
- Can add multiple backend instances
- MongoDB scales horizontally
- Groq API handles high volume
- Consider batch processing for very large volumes

### Design Questions

**Q: Why MongoDB instead of PostgreSQL?**
A:
- Flexible schema for evolving data
- Native JSON storage (our data is JSON-heavy)
- Easy to add new fields
- Good for analytics queries
- Scales well for document storage

**Q: Why Next.js instead of plain React?**
A:
- Server-side rendering for better SEO
- File-based routing (cleaner)
- Built-in API routes (if needed)
- Better performance
- Great developer experience

**Q: How would you improve this system?**
A:
- Add real-time streaming transcription
- Implement caching for repeated files
- Add batch processing for large volumes
- GPU acceleration for local Whisper
- Webhooks for async notifications
- Export to PDF/Excel
- Advanced filtering and search
- Multi-user collaboration features

---

## 🎓 Key Takeaways for Interviews

1. **Problem-Solution Fit**: Clearly explain the problem and how your solution addresses it
2. **Architecture**: Understand the three-tier architecture and data flow
3. **AI Pipeline**: Know each step: transcribe → translate → analyze → insights
4. **Design Decisions**: Justify why you chose each technology
5. **Performance**: Emphasize the 10-20x speed improvement with Groq
6. **Reliability**: Highlight the fallback system for 100% uptime
7. **Scalability**: Discuss how the system can scale
8. **Trade-offs**: Be ready to discuss pros/cons of your choices

---

**Good luck with your interviews! 🚀**

