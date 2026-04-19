"""
Audio Processing Pipeline - Clean & Simple

FLOW:
Audio File → Transcribe → Translate → LLM Analysis → Save Results

FEATURES:
- Groq Whisper API (fast) with local fallback
- Hindi/English translation
- LLM-powered intelligence analysis
- Sequential processing for stability
"""

import whisper
from transformers import MarianMTModel, MarianTokenizer
from pathlib import Path
import os
import warnings
import json
import time
import threading
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from collections import Counter

# Suppress warnings for clean output
warnings.filterwarnings("ignore")
load_dotenv()

# Thread lock for Whisper (PyTorch is not thread-safe)
whisper_lock = threading.Lock()


# ============================================================================
# STEP 0: LOAD MODELS ONCE AT STARTUP
# ============================================================================

print("🔧 Loading models...")

# Load Whisper model for transcription
whisper_model = whisper.load_model(os.getenv("WHISPER_MODEL", "medium"))
print(f"✅ Whisper loaded")

# Load translator for Hindi→English
try:
    translator_tokenizer = MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-hi-en")
    translator_model = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-hi-en")
    print("✅ Translator loaded")
except Exception as e:
    translator_model = None
    translator_tokenizer = None
    print(f"⚠️ Translator failed: {e}")

# Load Groq client for LLM and Whisper API
try:
    from groq import Groq
    groq_api_key = os.getenv("GROQ_API_KEY")
    if groq_api_key and groq_api_key != "your-groq-api-key-here":
        groq_client = Groq(api_key=groq_api_key)
        print("✅ Groq client loaded")
    else:
        groq_client = None
        print("⚠️ Groq API key missing")
except Exception as e:
    groq_client = None
    print(f"⚠️ Groq failed: {e}")

print("🎉 Models ready!\n")


# ============================================================================
# STEP 1: TRANSCRIPTION (Groq API with local fallback)
# ============================================================================

def transcribe(audio_path):
    """
    Transcribe audio file to text.
    
    Strategy:
    1. Try Groq Whisper API (fast, 3-10 seconds)
    2. If fails, use local Whisper (slower, 40-90 seconds)
    
    Returns: (transcript_dict, method_used, time_taken)
    """
    
    # Try Groq API first (fast cloud transcription)
    if groq_client:
        try:
            print("  ⚡ Trying Groq Whisper API...")
            start_time = time.time()
            
            with open(audio_path, "rb") as audio_file:
                response = groq_client.audio.transcriptions.create(
                    file=(audio_path.name, audio_file.read()),
                    model="whisper-large-v3",
                    response_format="verbose_json",
                    language="hi",
                    temperature=0.0
                )
            
            # Convert response to standard format
            transcript = {
                "text": response.text,
                "language": getattr(response, "language", "hi"),
                "segments": []
            }
            
            # Extract segments if available
            if hasattr(response, "segments") and response.segments:
                for seg in response.segments:
                    transcript["segments"].append({
                        "start": seg.get("start", 0),
                        "end": seg.get("end", 0),
                        "text": seg.get("text", ""),
                        "no_speech_prob": 0.0
                    })
            else:
                # Create single segment if no segments provided
                transcript["segments"] = [{
                    "start": 0.0,
                    "end": 0.0,
                    "text": response.text,
                    "no_speech_prob": 0.0
                }]
            
            elapsed = time.time() - start_time
            print(f"  ✅ Groq transcription: {elapsed:.2f}s")
            return transcript, "groq", elapsed
            
        except Exception as e:
            print(f"  ⚠️ Groq failed: {e}")
            print("  🔁 Falling back to local Whisper...")
    
    # Fallback to local Whisper
    start_time = time.time()
    with whisper_lock:  # Thread-safe access
        transcript = whisper_model.transcribe(
            str(audio_path.absolute()),
            language="hi",
            task="transcribe",
            temperature=0.0,
            beam_size=5,
            best_of=5,
            condition_on_previous_text=False,
            compression_ratio_threshold=2.4,
            logprob_threshold=-1.0,
            no_speech_threshold=0.6
        )
    
    elapsed = time.time() - start_time
    print(f"  ✅ Local transcription: {elapsed:.2f}s")
    return transcript, "local", elapsed


# ============================================================================
# STEP 2: TRANSLATION (Hindi → English)
# ============================================================================

def translate(text, source_language):
    """
    Translate text from Hindi/Urdu to English.
    
    Returns: tran
            start = time.time()
            result = transcribe_local(audio_path)
            elapsed = time.time() - start
            print(f"  ✅ Local transcription: {elapsed:.2f}s")
            return result, "local", elapsed
        
        except Exception as local_error:
            raise Exception(f"Both transcription methods failed. Groq: {e}, Local: {local_error}")

def translate_full_text(text: str, source_lang: str) -> Optional[str]:
    """
    Translate full transcript ONCE (not per segment).
    Much faster than translating each segment separately.
    """
    if source_lang == "en" or not text.strip():
        return None
    
    # Treat Urdu as Hindi
    if source_lang == "ur":
        source_lang = "hi"
    
    if translator_model is None or translator_tokenizer is None:
        return None
    
    try:
        # Split into chunks if too long (max 512 tokens)
        max_length = 400  # Leave room for tokenization
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0
        
        for word in words:
            current_length += len(word) + 1
            if current_length > max_length:
                chunks.append(' '.join(current_chunk))
                current_chunk = [word]
                current_length = len(word)
            else:
                current_chunk.append(word)
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        # Translate all chunks
        translated_chunks = []
        for chunk in chunks:
            inputs = translator_tokenizer(chunk, return_tensors="pt", padding=True, truncation=True, max_length=512)
            translated = translator_model.generate(**inputs)
            translated_text = translator_tokenizer.decode(translated[0], skip_special_tokens=True)
            translated_chunks.append(translated_text)
        
        return ' '.join(translated_chunks)
    
    except Exception as e:
        print(f"  ⚠️ Translation failed: {e}")
        return None


def analyze_with_llm(text: str, original_text: str = None) -> Optional[Dict]:
    """
    Analyze FULL transcript with LLM (not per segment).
    Returns file-level intelligence.
    """
    if groq_client is None:
        return None
    
    try:
        context_note = ""
        if original_text and original_text != text:
            context_note = f"\n\nOriginal text (Hindi/Hinglish): \"{original_text[:500]}...\""
        
        prompt = f"""You are an advanced audio intelligence system analyzing a customer service call recording.

Full transcript: "{text[:2000]}..."{context_note}

Analyze this ENTIRE conversation and provide comprehensive intelligence.

Return JSON with this EXACT structure:
{{
  "overall_sentiment": {{
    "type": "one of: positive, negative, neutral, aggressive, frustrated, fearful, anxious, angry, disappointed, satisfied",
    "intensity": 0.0 to 1.0
  }},
  "primary_intent": "the main purpose of this call (be specific)",
  "priority": "one of: low, medium, high, critical",
  "risk_level": "one of: low, moderate, high, extreme",
  "urgency": "one of: low, medium, high, immediate",
  "key_events": ["array of main events: complaint, threat, refund_demand, technical_issue, etc."],
  "entities": ["important entities: names, products, amounts, dates"],
  "target": "who/what is being targeted or null",
  "summary": "2-3 sentence summary of the entire conversation and why it matters",
  "confidence": 0.0 to 1.0
}}

Return ONLY valid JSON, no markdown:"""

        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are an advanced audio intelligence system. Analyze conversations deeply. Always respond with valid JSON only."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=1000,
            timeout=10.0
        )
        
        content = response.choices[0].message.content.strip()
        
        # Extract JSON
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        
        result = json.loads(content)
        
        # Validate structure
        if not isinstance(result.get("overall_sentiment"), dict):
            sentiment_type = result.get("overall_sentiment", "neutral")
            result["overall_sentiment"] = {
                "type": sentiment_type,
                "intensity": 0.7
            }
        
        return result
    
    except Exception as e:
        print(f"  ⚠️ LLM analysis failed: {e}")
        return None


def create_segments_from_whisper(whisper_result: dict, file_level_analysis: dict) -> List[dict]:
    """
    Create segment data from Whisper output + file-level LLM analysis.
    Each segment inherits intelligence from file-level analysis.
    """
    segments = []
    
    for seg in whisper_result["segments"]:
        text = seg["text"].strip()
        
        # Skip very short or low-confidence segments
        if len(text) < 5 or seg.get("no_speech_prob", 0) > 0.8:
            continue
        
        # Build segment with file-level intelligence
        segment_data = {
            "start": round(seg["start"], 2),
            "end": round(seg["end"], 2),
            "text": text,
            "language": whisper_result.get("language", "hi"),
            
            # Inherit from file-level analysis
            "events": file_level_analysis.get("key_events", ["general"]),
            "sentiment": file_level_analysis.get("overall_sentiment", {}).get("type", "neutral"),
            "sentiment_intensity": file_level_analysis.get("overall_sentiment", {}).get("intensity", 0.5),
            "intent": file_level_analysis.get("primary_intent", "general_query"),
            "priority": file_level_analysis.get("priority", "medium"),
            "risk_level": file_level_analysis.get("risk_level", "low"),
            "urgency": file_level_analysis.get("urgency", "medium"),
            "entities": file_level_analysis.get("entities", []),
            "confidence": file_level_analysis.get("confidence", 0.8),
            "summary": file_level_analysis.get("summary", ""),
            "analysis_source": "llm"
        }
        
        if file_level_analysis.get("target"):
            segment_data["target"] = file_level_analysis["target"]
        
        segments.append(segment_data)
    
    return segments


def process_single_file(file_record: dict, cluster_id: str) -> dict:
    """
    Process a single audio file with optimized pipeline.
    
    PIPELINE:
    1. Transcribe with Whisper (medium)
    2. Translate ONCE (full transcript)
    3. Analyze with LLM ONCE (full transcript)
    4. Create segments with file-level intelligence
    """
    file_start = time.time()
    
    try:
        print(f"\n🔄 Processing: {file_record['file_name']}")
        
        # Get file path - stored as "uploads/{cluster_id}/{filename}"
        file_path_str = file_record["file_path"]
        
        # Resolve path relative to backend directory
        # The script is in backend/services/processor.py
        # Files are in backend/uploads/
        backend_dir = Path(__file__).parent.parent  # Go up from services/ to backend/
        file_path = backend_dir / file_path_str
        
        print(f"  📁 Looking for: {file_path}")
        
        if not file_path.exists():
            print(f"  ❌ File not found at: {file_path}")
            print(f"     Backend dir: {backend_dir}")
            print(f"     Relative path: {file_path_str}")
            raise FileNotFoundError(f"Audio file not found: {file_path}")
        
        # STEP 1: Transcribe with Groq API (with local fallback)
        print(f"  🎤 Transcribing...")
        transcribe_start = time.time()
        
        result, transcribe_method, transcribe_time = transcribe(file_path)
        
        print(f"  ✅ Transcribed in {transcribe_time:.2f}s using {transcribe_method} ({len(result.get('segments', []))} segments)")
        
        detected_language = result.get("language", "hi")
        full_transcript = result.get("text", "").strip()
        
        if not full_transcript:
            raise ValueError("Empty transcription")
        
        # STEP 2: Translate ONCE (full transcript)
        translate_start = time.time()
        translated_transcript = None
        analysis_text = full_transcript
        
        if detected_language != "en":
            print(f"  🌐 Translating full transcript...")
            translated_transcript = translate_full_text(full_transcript, detected_language)
            if translated_transcript:
                analysis_text = translated_transcript
                print(f"  ✅ Translated in {time.time() - translate_start:.2f}s")
        
        # STEP 3: Analyze with LLM ONCE (full transcript)
        print(f"  ✨ Analyzing with LLM...")
        llm_start = time.time()
        
        file_level_analysis = analyze_with_llm(analysis_text, full_transcript)
        
        if file_level_analysis:
            llm_time = time.time() - llm_start
            print(f"  ✅ LLM analysis in {llm_time:.2f}s")
        else:
            print(f"  ⚠️ LLM failed, using basic analysis")
            file_level_analysis = {
                "overall_sentiment": {"type": "neutral", "intensity": 0.5},
                "primary_intent": "general_query",
                "priority": "medium",
                "risk_level": "low",
                "urgency": "medium",
                "key_events": ["general"],
                "entities": [],
                "target": None,
                "summary": "Customer service interaction",
                "confidence": 0.5
            }
        
        # STEP 4: Create segments with file-level intelligence
        segments = create_segments_from_whisper(result, file_level_analysis)
        
        # Add translated text to segments if available
        if translated_transcript:
            for seg in segments:
                seg["translated_text"] = translated_transcript
        
        # Calculate file summary
        total_segments = len(segments)
        negative_count = sum(1 for s in segments if s["sentiment"] in ["negative", "aggressive", "frustrated", "angry"])
        high_priority_count = sum(1 for s in segments if s["priority"] in ["high", "critical"])
        
        file_summary = {
            "total_segments": total_segments,
            "negative_percentage": round((negative_count / total_segments * 100) if total_segments > 0 else 0, 1),
            "high_priority_count": high_priority_count,
            "top_issue": file_level_analysis.get("key_events", ["general"])[0] if file_level_analysis.get("key_events") else "general",
            "overall_sentiment": file_level_analysis.get("overall_sentiment", {}).get("type", "neutral"),
            "language": detected_language
        }
        
        total_time = time.time() - file_start
        print(f"  ✅ Completed in {total_time:.2f}s (Transcribe[{transcribe_method}]: {transcribe_time:.2f}s)")
        
        return {
            "file_id": str(file_record["_id"]),
            "file_name": file_record["file_name"],
            "cluster_id": cluster_id,
            "segments": segments,
            "summary": file_summary,
            "language": detected_language,
            "processing_time": {
                "total": round(total_time, 2),
                "transcription": round(transcribe_time, 2),
                "transcription_method": transcribe_method
            },
            "status": "success"
        }
    
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
        return {
            "file_id": str(file_record["_id"]),
            "file_name": file_record["file_name"],
            "cluster_id": cluster_id,
            "status": "failed",
            "error": str(e)
        }


async def process_cluster(cluster_id: str, files: List[dict]):
    """
    Process all files in a cluster using ThreadPoolExecutor.
    
    OPTIMIZED APPROACH:
    - No multiprocessing (Whisper medium is heavy)
    - ThreadPoolExecutor with max_workers=1 (Whisper is thread-locked for safety)
    - All models loaded once globally
    - Each thread reuses same models
    """
    print(f"\n🚀 Processing {len(files)} files for cluster {cluster_id}")
    print(f"📊 Processing files sequentially (Whisper requires thread lock)")
    
    # Connect to DB
    db_client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
    db = db_client[os.getenv("MONGODB_DB_NAME", "sarcis")]
    
    # Mark files as processing
    for file in files:
        await db.files.update_one(
            {"_id": ObjectId(file["_id"])},
            {"$set": {"status": "processing"}}
        )
    
    # Process files sequentially (Whisper is thread-locked anyway)
    cluster_start = time.time()
    
    # Process one at a time since Whisper uses a lock
    results = []
    for file in files:
        result = process_single_file(file, cluster_id)
        results.append(result)
    
    cluster_time = time.time() - cluster_start
    print(f"\n✅ All files processed in {cluster_time:.2f}s")
    
    # Save results to database
    for result in results:
        if result["status"] == "success":
            # Check if result exists
            existing = await db.results.find_one({
                "cluster_id": result["cluster_id"],
                "file_id": result["file_id"]
            })
            
            if existing:
                await db.results.update_one(
                    {"_id": existing["_id"]},
                    {"$set": {
                        "segments": result["segments"],
                        "summary": result["summary"],
                        "language": result.get("language", "en")
                    }}
                )
            else:
                await db.results.insert_one({
                    "cluster_id": result["cluster_id"],
                    "file_id": result["file_id"],
                    "file_name": result["file_name"],
                    "segments": result["segments"],
                    "summary": result["summary"],
                    "language": result.get("language", "en")
                })
            
            # Update file status
            await db.files.update_one(
                {"_id": ObjectId(result["file_id"])},
                {"$set": {"status": "done"}}
            )
        else:
            await db.files.update_one(
                {"_id": ObjectId(result["file_id"])},
                {"$set": {"status": "failed", "error": result.get("error", "Unknown error")}}
            )
    
    # Calculate cluster insights
    await calculate_cluster_insights(cluster_id, db)
    
    print(f"🎉 Cluster processing complete!")
    
    db_client.close()


async def calculate_cluster_insights(cluster_id: str, db):
    """Calculate aggregated cluster-level insights"""
    results = await db.results.find({"cluster_id": cluster_id}).to_list(1000)
    
    if not results:
        return
    
    total_files = len(results)
    total_segments = sum(len(r["segments"]) for r in results)
    
    # Aggregate metrics
    all_events = []
    all_sentiments = []
    all_priorities = []
    all_intents = []
    
    for result in results:
        for segment in result["segments"]:
            all_events.extend(segment["events"])
            all_sentiments.append(segment["sentiment"])
            all_priorities.append(segment["priority"])
            all_intents.append(segment["intent"])
    
    from collections import Counter
    
    event_counts = Counter(all_events)
    sentiment_counts = Counter(all_sentiments)
    priority_counts = Counter(all_priorities)
    intent_counts = Counter(all_intents)
    
    # Calculate percentages
    complaint_percentage = round((event_counts.get("complaint", 0) / total_segments * 100) if total_segments > 0 else 0, 1)
    urgency_percentage = round((event_counts.get("urgency", 0) / total_segments * 100) if total_segments > 0 else 0, 1)
    negative_percentage = round((sentiment_counts.get("negative", 0) / total_segments * 100) if total_segments > 0 else 0, 1)
    high_priority_percentage = round(((priority_counts.get("high", 0) + priority_counts.get("critical", 0)) / total_segments * 100) if total_segments > 0 else 0, 1)
    
    insights = {
        "cluster_id": cluster_id,
        "total_files": total_files,
        "total_segments": total_segments,
        "complaint_percentage": complaint_percentage,
        "urgency_percentage": urgency_percentage,
        "negative_percentage": negative_percentage,
        "high_priority_percentage": high_priority_percentage,
        "top_events": dict(event_counts.most_common(5)),
        "top_intents": dict(intent_counts.most_common(5)),
        "sentiment_distribution": dict(sentiment_counts),
        "priority_distribution": dict(priority_counts)
    }
    
    # Save insights
    await db.cluster_insights.update_one(
        {"cluster_id": cluster_id},
        {"$set": insights},
        upsert=True
    )
    
    print(f"📊 Cluster insights calculated")
