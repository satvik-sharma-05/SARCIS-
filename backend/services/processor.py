"""
Audio Processing Pipeline - Clean & Interview-Friendly

SIMPLE FLOW:
Audio File → Transcribe → Translate → LLM Analysis → Save Results

FEATURES:
- Groq Whisper API (fast) with local Whisper fallback
- Hindi/English translation
- LLM-powered intelligence
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

# Clean console output
warnings.filterwarnings("ignore")
load_dotenv()

# Thread lock for Whisper (PyTorch is not thread-safe)
whisper_lock = threading.Lock()


# ============================================================================
# STEP 0: LOAD MODELS ONCE AT STARTUP
# ============================================================================

print("🔧 Loading models...")

# Whisper for transcription
whisper_model = whisper.load_model(os.getenv("WHISPER_MODEL", "medium"))
print("✅ Whisper loaded")

# Translator for Hindi→English
try:
    translator_tokenizer = MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-hi-en")
    translator_model = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-hi-en")
    print("✅ Translator loaded")
except Exception as e:
    translator_model = None
    translator_tokenizer = None
    print(f"⚠️ Translator failed: {e}")

# Groq client for LLM and Whisper API
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
    
    Returns: translated_text or None
    """
    # Skip if already English or empty
    if source_language == "en" or not text.strip():
        return None
    
    # Treat Urdu as Hindi
    if source_language == "ur":
        source_language = "hi"
    
    # Check if translator is available
    if not translator_model or not translator_tokenizer:
        return None
    
    try:
        # Split long text into chunks (max 400 words per chunk)
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0
        max_length = 400
        
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
        
        # Translate each chunk
        translated_chunks = []
        for chunk in chunks:
            inputs = translator_tokenizer(
                chunk,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512
            )
            translated = translator_model.generate(**inputs)
            translated_text = translator_tokenizer.decode(translated[0], skip_special_tokens=True)
            translated_chunks.append(translated_text)
        
        return ' '.join(translated_chunks)
    
    except Exception as e:
        print(f"  ⚠️ Translation failed: {e}")
        return None


# ============================================================================
# STEP 3: LLM ANALYSIS (Extract intelligence from transcript)
# ============================================================================

def analyze_with_llm(text, original_text=None):
    """
    Analyze full transcript with LLM to extract intelligence.
    
    Returns: analysis_dict with sentiment, intent, risk, etc.
    """
    if not groq_client:
        return None
    
    try:
        # Add context if we have original Hindi text
        context_note = ""
        if original_text and original_text != text:
            context_note = f"\n\nOriginal (Hindi): \"{original_text[:500]}...\""
        
        # Prompt for LLM
        prompt = f"""You are an AI analyzing a customer service call.

Transcript: "{text[:2000]}..."{context_note}

Analyze this conversation and return JSON with:
{{
  "overall_sentiment": {{
    "type": "positive/negative/neutral/aggressive/frustrated/fearful/anxious/angry/disappointed/satisfied",
    "intensity": 0.0 to 1.0
  }},
  "primary_intent": "main purpose of call",
  "priority": "low/medium/high/critical",
  "risk_level": "low/moderate/high/extreme",
  "urgency": "low/medium/high/immediate",
  "key_events": ["complaint", "threat", "refund_demand", etc.],
  "entities": ["names", "products", "amounts", "dates"],
  "target": "who/what is targeted or null",
  "summary": "2-3 sentence summary",
  "confidence": 0.0 to 1.0
}}

Return ONLY valid JSON:"""

        # Call LLM
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an AI that analyzes conversations. Always return valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=1000,
            timeout=10.0
        )
        
        # Extract JSON from response
        content = response.choices[0].message.content.strip()
        
        # Remove markdown code blocks if present
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        
        # Parse JSON
        analysis = json.loads(content)
        
        # Validate sentiment structure
        if not isinstance(analysis.get("overall_sentiment"), dict):
            sentiment_type = analysis.get("overall_sentiment", "neutral")
            analysis["overall_sentiment"] = {
                "type": sentiment_type,
                "intensity": 0.7
            }
        
        return analysis
    
    except Exception as e:
        print(f"  ⚠️ LLM analysis failed: {e}")
        return None


# ============================================================================
# STEP 4: CREATE SEGMENTS (Combine transcription + analysis)
# ============================================================================

def create_segments(transcript, file_analysis):
    """
    Create segments from transcript and apply file-level analysis to each.
    
    Each segment inherits intelligence from the file-level analysis.
    """
    segments = []
    
    for seg in transcript["segments"]:
        text = seg["text"].strip()
        
        # Skip very short or low-confidence segments
        if len(text) < 5 or seg.get("no_speech_prob", 0) > 0.8:
            continue
        
        # Build segment with file-level intelligence
        segment = {
            "start": round(seg["start"], 2),
            "end": round(seg["end"], 2),
            "text": text,
            "language": transcript.get("language", "hi"),
            
            # Intelligence from file-level analysis
            "events": file_analysis.get("key_events", ["general"]),
            "sentiment": file_analysis.get("overall_sentiment", {}).get("type", "neutral"),
            "sentiment_intensity": file_analysis.get("overall_sentiment", {}).get("intensity", 0.5),
            "intent": file_analysis.get("primary_intent", "general_query"),
            "priority": file_analysis.get("priority", "medium"),
            "risk_level": file_analysis.get("risk_level", "low"),
            "urgency": file_analysis.get("urgency", "medium"),
            "entities": file_analysis.get("entities", []),
            "confidence": file_analysis.get("confidence", 0.8),
            "summary": file_analysis.get("summary", ""),
            "analysis_source": "llm"
        }
        
        # Add target if present
        if file_analysis.get("target"):
            segment["target"] = file_analysis["target"]
        
        segments.append(segment)
    
    return segments


# ============================================================================
# STEP 5: PROCESS SINGLE FILE (Main pipeline)
# ============================================================================

def process_file(file_record, cluster_id):
    """
    Process a single audio file through the complete pipeline.
    
    Pipeline:
    1. Transcribe audio (Groq API or local Whisper)
    2. Translate to English (if needed)
    3. Analyze with LLM
    4. Create segments with intelligence
    5. Return results
    """
    start_time = time.time()
    
    try:
        print(f"\n🔄 Processing: {file_record['file_name']}")
        
        # Get file path
        file_path_str = file_record["file_path"]
        backend_dir = Path(__file__).parent.parent
        file_path = backend_dir / file_path_str
        
        print(f"  📁 Path: {file_path}")
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # STEP 1: Transcribe
        print("  🎤 Transcribing...")
        transcript, method, transcribe_time = transcribe(file_path)
        
        detected_language = transcript.get("language", "hi")
        full_text = transcript.get("text", "").strip()
        
        if not full_text:
            raise ValueError("Empty transcription")
        
        print(f"  ✅ Transcribed using {method} ({len(transcript['segments'])} segments)")
        
        # STEP 2: Translate (if not English)
        translated_text = None
        analysis_text = full_text
        
        if detected_language != "en":
            print("  🌐 Translating...")
            translate_start = time.time()
            translated_text = translate(full_text, detected_language)
            if translated_text:
                analysis_text = translated_text
                print(f"  ✅ Translated in {time.time() - translate_start:.2f}s")
        
        # STEP 3: Analyze with LLM
        print("  ✨ Analyzing with LLM...")
        llm_start = time.time()
        file_analysis = analyze_with_llm(analysis_text, full_text)
        
        if file_analysis:
            print(f"  ✅ LLM analysis in {time.time() - llm_start:.2f}s")
        else:
            # Fallback analysis if LLM fails
            print("  ⚠️ LLM failed, using basic analysis")
            file_analysis = {
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
        
        # STEP 4: Create segments
        segments = create_segments(transcript, file_analysis)
        
        # Add translated text to segments if available
        if translated_text:
            for seg in segments:
                seg["translated_text"] = translated_text
        
        # Calculate file summary
        total_segments = len(segments)
        negative_count = sum(1 for s in segments if s["sentiment"] in ["negative", "aggressive", "frustrated", "angry"])
        high_priority_count = sum(1 for s in segments if s["priority"] in ["high", "critical"])
        
        file_summary = {
            "total_segments": total_segments,
            "negative_percentage": round((negative_count / total_segments * 100) if total_segments > 0 else 0, 1),
            "high_priority_count": high_priority_count,
            "top_issue": file_analysis.get("key_events", ["general"])[0] if file_analysis.get("key_events") else "general",
            "overall_sentiment": file_analysis.get("overall_sentiment", {}).get("type", "neutral"),
            "language": detected_language
        }
        
        total_time = time.time() - start_time
        print(f"  ✅ Completed in {total_time:.2f}s")
        
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
                "transcription_method": method
            },
            "status": "success"
        }
    
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return {
            "file_id": str(file_record["_id"]),
            "file_name": file_record["file_name"],
            "cluster_id": cluster_id,
            "status": "failed",
            "error": str(e)
        }


# ============================================================================
# STEP 6: PROCESS CLUSTER (Process multiple files)
# ============================================================================

async def process_cluster(cluster_id, files):
    """
    Process all files in a cluster sequentially.
    
    Sequential processing ensures stability with Whisper model.
    """
    print(f"\n🚀 Processing {len(files)} files for cluster {cluster_id}")
    
    # Connect to database
    db_client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
    db = db_client[os.getenv("MONGODB_DB_NAME", "sarcis")]
    
    # Mark files as processing
    for file in files:
        await db.files.update_one(
            {"_id": ObjectId(file["_id"])},
            {"$set": {"status": "processing"}}
        )
    
    # Process files one by one
    cluster_start = time.time()
    results = []
    
    for file in files:
        result = process_file(file, cluster_id)
        results.append(result)
    
    cluster_time = time.time() - cluster_start
    print(f"\n✅ All files processed in {cluster_time:.2f}s")
    
    # Save results to database
    for result in results:
        if result["status"] == "success":
            # Check if result already exists
            existing = await db.results.find_one({
                "cluster_id": result["cluster_id"],
                "file_id": result["file_id"]
            })
            
            if existing:
                # Update existing result
                await db.results.update_one(
                    {"_id": existing["_id"]},
                    {"$set": {
                        "segments": result["segments"],
                        "summary": result["summary"],
                        "language": result.get("language", "en")
                    }}
                )
            else:
                # Insert new result
                await db.results.insert_one({
                    "cluster_id": result["cluster_id"],
                    "file_id": result["file_id"],
                    "file_name": result["file_name"],
                    "segments": result["segments"],
                    "summary": result["summary"],
                    "language": result.get("language", "en")
                })
            
            # Update file status to done
            await db.files.update_one(
                {"_id": ObjectId(result["file_id"])},
                {"$set": {"status": "done"}}
            )
        else:
            # Update file status to failed
            await db.files.update_one(
                {"_id": ObjectId(result["file_id"])},
                {"$set": {"status": "failed", "error": result.get("error", "Unknown error")}}
            )
    
    # Calculate cluster insights
    await calculate_insights(cluster_id, db)
    
    print("🎉 Cluster processing complete!")
    db_client.close()


# ============================================================================
# STEP 7: CALCULATE INSIGHTS (Aggregate cluster statistics)
# ============================================================================

async def calculate_insights(cluster_id, db):
    """
    Calculate aggregated insights for the entire cluster.
    
    Aggregates: events, sentiments, priorities, intents
    """
    # Get all results for this cluster
    results = await db.results.find({"cluster_id": cluster_id}).to_list(1000)
    
    if not results:
        return
    
    total_files = len(results)
    total_segments = sum(len(r["segments"]) for r in results)
    
    # Collect all data
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
    
    # Count occurrences
    event_counts = Counter(all_events)
    sentiment_counts = Counter(all_sentiments)
    priority_counts = Counter(all_priorities)
    intent_counts = Counter(all_intents)
    
    # Calculate percentages
    complaint_pct = round((event_counts.get("complaint", 0) / total_segments * 100) if total_segments > 0 else 0, 1)
    urgency_pct = round((event_counts.get("urgency", 0) / total_segments * 100) if total_segments > 0 else 0, 1)
    negative_pct = round((sentiment_counts.get("negative", 0) / total_segments * 100) if total_segments > 0 else 0, 1)
    high_priority_pct = round(((priority_counts.get("high", 0) + priority_counts.get("critical", 0)) / total_segments * 100) if total_segments > 0 else 0, 1)
    
    # Build insights object
    insights = {
        "cluster_id": cluster_id,
        "total_files": total_files,
        "total_segments": total_segments,
        "complaint_percentage": complaint_pct,
        "urgency_percentage": urgency_pct,
        "negative_percentage": negative_pct,
        "high_priority_percentage": high_priority_pct,
        "top_events": dict(event_counts.most_common(5)),
        "top_intents": dict(intent_counts.most_common(5)),
        "sentiment_distribution": dict(sentiment_counts),
        "priority_distribution": dict(priority_counts)
    }
    
    # Save to database
    await db.cluster_insights.update_one(
        {"cluster_id": cluster_id},
        {"$set": insights},
        upsert=True
    )
    
    print("📊 Cluster insights calculated")
