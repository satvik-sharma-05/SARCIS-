"""
Smart Audio Risk & Context Intelligence System - Backend
Clean MVP with MongoDB
"""
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import FileResponse
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime, timedelta, timezone
import os
from pathlib import Path
import shutil

# Import our modules
from db import get_db, init_db
from models import User, Cluster, FileRecord, Result
from services.auth import hash_password, verify_password, create_access_token, verify_token
from services.processor import process_cluster

# ============= STARTUP =============
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    print("✅ Database connected")
    yield
    # Shutdown (if needed)

app = FastAPI(title="SARCIS API", lifespan=lifespan)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

# Ensure uploads directory exists
UPLOAD_DIR = Path(__file__).parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


# ============= MODELS =============
class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    name: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ClusterCreate(BaseModel):
    name: str


# ============= AUTH DEPENDENCY =============
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    db = await get_db()
    from bson import ObjectId
    
    try:
        user_id = ObjectId(payload["user_id"])
    except:
        raise HTTPException(status_code=401, detail="Invalid user ID")
    
    user = await db.users.find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user


# ============= AUTH ROUTES =============
@app.post("/auth/signup")
async def signup(req: SignupRequest):
    db = await get_db()
    
    # Check if user exists
    existing = await db.users.find_one({"email": req.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user
    user = {
        "email": req.email,
        "name": req.name,
        "password": hash_password(req.password),
        "created_at": datetime.now(timezone.utc)
    }
    result = await db.users.insert_one(user)
    user_id = str(result.inserted_id)
    
    # Generate token
    token = create_access_token({"user_id": user_id, "email": req.email})
    
    return {
        "access_token": token,
        "user": {"id": user_id, "email": req.email, "name": req.name}
    }


@app.post("/auth/login")
async def login(req: LoginRequest):
    db = await get_db()
    
    user = await db.users.find_one({"email": req.email})
    if not user or not verify_password(req.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user_id = str(user["_id"])
    token = create_access_token({"user_id": user_id, "email": user["email"]})
    
    return {
        "access_token": token,
        "user": {"id": user_id, "email": user["email"], "name": user["name"]}
    }


# ============= CLUSTER ROUTES =============
@app.get("/clusters")
async def get_clusters(user = Depends(get_current_user)):
    db = await get_db()
    user_id = str(user["_id"])
    
    clusters = await db.clusters.find({"user_id": user_id}).to_list(100)
    
    # Get file counts
    for cluster in clusters:
        cluster_id_str = str(cluster["_id"])
        cluster["id"] = cluster_id_str
        del cluster["_id"]
        file_count = await db.files.count_documents({"cluster_id": cluster_id_str})
        cluster["file_count"] = file_count
    
    return {"clusters": clusters}


@app.post("/clusters")
async def create_cluster(req: ClusterCreate, user = Depends(get_current_user)):
    db = await get_db()
    user_id = str(user["_id"])
    
    cluster = {
        "user_id": user_id,
        "name": req.name,
        "created_at": datetime.now(timezone.utc),
        "status": "active"
    }
    result = await db.clusters.insert_one(cluster)
    cluster["id"] = str(result.inserted_id)
    del cluster["_id"]
    cluster["file_count"] = 0
    
    return cluster


@app.delete("/clusters/{cluster_id}")
async def delete_cluster(cluster_id: str, user = Depends(get_current_user)):
    db = await get_db()
    user_id = str(user["_id"])
    
    from bson import ObjectId
    
    # Verify ownership
    try:
        cluster_obj_id = ObjectId(cluster_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid cluster ID")
    
    cluster = await db.clusters.find_one({"_id": cluster_obj_id, "user_id": user_id})
    if not cluster:
        raise HTTPException(status_code=404, detail="Cluster not found")
    
    # Delete files from disk
    files = await db.files.find({"cluster_id": cluster_id}).to_list(1000)
    for file in files:
        file_path = Path(file["file_path"])
        if file_path.exists():
            file_path.unlink()
    
    # Delete from database
    await db.files.delete_many({"cluster_id": cluster_id})
    await db.results.delete_many({"cluster_id": cluster_id})
    await db.clusters.delete_one({"_id": cluster_obj_id})
    
    return {"message": "Cluster deleted"}


# ============= FILE ROUTES =============
@app.post("/upload")
async def upload_files(
    cluster_id: str = Form(...),
    files: List[UploadFile] = File(...),
    user = Depends(get_current_user)
):
    db = await get_db()
    user_id = str(user["_id"])
    
    from bson import ObjectId
    
    # Verify cluster ownership
    try:
        cluster_obj_id = ObjectId(cluster_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid cluster ID")
    
    cluster = await db.clusters.find_one({"_id": cluster_obj_id, "user_id": user_id})
    if not cluster:
        raise HTTPException(status_code=404, detail="Cluster not found")
    
    uploaded_files = []
    
    for file in files:
        # Save file
        cluster_dir = UPLOAD_DIR / cluster_id
        cluster_dir.mkdir(exist_ok=True)
        
        file_path = cluster_dir / file.filename
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Save metadata
        file_record = {
            "cluster_id": cluster_id,
            "file_name": file.filename,
            "file_path": f"uploads/{cluster_id}/{file.filename}",  # Store relative path
            "uploaded_at": datetime.now(timezone.utc),
            "status": "pending"  # Track processing status
        }
        result = await db.files.insert_one(file_record)
        file_record["id"] = str(result.inserted_id)
        del file_record["_id"]
        
        uploaded_files.append(file_record)
    
    return {"files": uploaded_files}


@app.get("/clusters/{cluster_id}/files")
async def get_cluster_files(cluster_id: str, user = Depends(get_current_user)):
    db = await get_db()
    user_id = str(user["_id"])
    
    from bson import ObjectId
    
    # Verify cluster ownership
    try:
        cluster_obj_id = ObjectId(cluster_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid cluster ID")
    
    cluster = await db.clusters.find_one({"_id": cluster_obj_id, "user_id": user_id})
    if not cluster:
        raise HTTPException(status_code=404, detail="Cluster not found")
    
    files = await db.files.find({"cluster_id": cluster_id}).to_list(1000)
    
    for file in files:
        file["id"] = str(file["_id"])
        del file["_id"]
    
    return {"files": files}


# ============= ANALYSIS ROUTES =============
@app.post("/analyze/{cluster_id}")
async def analyze_cluster(cluster_id: str, user = Depends(get_current_user)):
    """Analyze cluster - only process new/unprocessed files (incremental)"""
    db = await get_db()
    user_id = str(user["_id"])
    
    from bson import ObjectId
    
    # Verify ownership
    try:
        cluster_obj_id = ObjectId(cluster_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid cluster ID")
    
    cluster = await db.clusters.find_one({"_id": cluster_obj_id, "user_id": user_id})
    if not cluster:
        raise HTTPException(status_code=404, detail="Cluster not found")
    
    # Get ONLY unprocessed files (incremental analysis)
    files = await db.files.find({
        "cluster_id": cluster_id,
        "status": {"$in": ["pending", "failed"]}  # Process pending or previously failed files
    }).to_list(1000)
    
    if not files:
        # All files already processed
        return {"message": "All files already analyzed", "files_processed": 0}
    
    print(f"📊 Processing {len(files)} new/unprocessed files (incremental analysis)")
    
    # Update cluster status
    await db.clusters.update_one(
        {"_id": cluster_obj_id},
        {"$set": {"status": "processing"}}
    )
    
    # Process files synchronously
    try:
        await process_cluster(cluster_id, files)
        
        # Update cluster status
        await db.clusters.update_one(
            {"_id": cluster_obj_id},
            {"$set": {"status": "completed", "processed_at": datetime.now(timezone.utc)}}
        )
        
        return {"message": "Analysis completed", "files_processed": len(files)}
    
    except Exception as e:
        await db.clusters.update_one(
            {"_id": cluster_obj_id},
            {"$set": {"status": "failed"}}
        )
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/reanalyze/{cluster_id}")
async def reanalyze_cluster(cluster_id: str, user = Depends(get_current_user)):
    """Re-analyze all files in cluster (force reprocessing)"""
    db = await get_db()
    user_id = str(user["_id"])
    
    from bson import ObjectId
    
    # Verify ownership
    try:
        cluster_obj_id = ObjectId(cluster_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid cluster ID")
    
    cluster = await db.clusters.find_one({"_id": cluster_obj_id, "user_id": user_id})
    if not cluster:
        raise HTTPException(status_code=404, detail="Cluster not found")
    
    # Reset all file statuses to pending
    await db.files.update_many(
        {"cluster_id": cluster_id},
        {"$set": {"status": "pending"}}
    )
    
    # Delete existing results
    await db.results.delete_many({"cluster_id": cluster_id})
    await db.cluster_insights.delete_many({"cluster_id": cluster_id})
    
    # Get all files
    files = await db.files.find({"cluster_id": cluster_id}).to_list(1000)
    
    if not files:
        raise HTTPException(status_code=400, detail="No files to process")
    
    print(f"🔄 Re-analyzing ALL {len(files)} files")
    
    # Update cluster status
    await db.clusters.update_one(
        {"_id": cluster_obj_id},
        {"$set": {"status": "processing"}}
    )
    
    # Process files
    try:
        await process_cluster(cluster_id, files)
        
        # Update cluster status
        await db.clusters.update_one(
            {"_id": cluster_obj_id},
            {"$set": {"status": "completed", "processed_at": datetime.now(timezone.utc)}}
        )
        
        return {"message": "Re-analysis completed", "files_processed": len(files)}
    
    except Exception as e:
        await db.clusters.update_one(
            {"_id": cluster_obj_id},
            {"$set": {"status": "failed"}}
        )
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/results/{cluster_id}")
async def get_results(cluster_id: str, user = Depends(get_current_user)):
    db = await get_db()
    user_id = str(user["_id"])
    
    from bson import ObjectId
    
    # Verify ownership
    try:
        cluster_obj_id = ObjectId(cluster_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid cluster ID")
    
    cluster = await db.clusters.find_one({"_id": cluster_obj_id, "user_id": user_id})
    if not cluster:
        raise HTTPException(status_code=404, detail="Cluster not found")
    
    # Get results
    results = await db.results.find({"cluster_id": cluster_id}).to_list(1000)
    
    for result in results:
        result["id"] = str(result["_id"])
        del result["_id"]
    
    return {"results": results}


@app.get("/clusters/{cluster_id}/insights")
async def get_cluster_insights(cluster_id: str, user = Depends(get_current_user)):
    """
    Get comprehensive cluster insights with rankings and analytics.
    Uses existing results data - no recomputation needed.
    """
    db = await get_db()
    user_id = str(user["_id"])
    
    from bson import ObjectId
    
    # Verify ownership
    try:
        cluster_obj_id = ObjectId(cluster_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid cluster ID")
    
    cluster = await db.clusters.find_one({"_id": cluster_obj_id, "user_id": user_id})
    if not cluster:
        raise HTTPException(status_code=404, detail="Cluster not found")
    
    # Get all results for this cluster
    results = await db.results.find({"cluster_id": cluster_id}).to_list(1000)
    
    if not results:
        return {"insights": None, "message": "No analysis results available"}
    
    # ============= COMPUTE INSIGHTS =============
    from collections import Counter
    
    # 1. Basic Metrics
    total_files = len(results)
    total_segments = sum(len(r.get("segments", [])) for r in results)
    
    # 2. Sentiment Distribution
    sentiment_counts = Counter()
    for result in results:
        for segment in result.get("segments", []):
            sentiment_counts[segment.get("sentiment", "neutral")] += 1
    
    sentiment_distribution = {
        "positive": sentiment_counts.get("positive", 0),
        "negative": sentiment_counts.get("negative", 0),
        "neutral": sentiment_counts.get("neutral", 0)
    }
    
    # Calculate percentages
    sentiment_percentages = {}
    if total_segments > 0:
        for sentiment, count in sentiment_distribution.items():
            sentiment_percentages[sentiment] = round((count / total_segments) * 100, 1)
    
    # 3. Event Distribution
    event_counts = Counter()
    for result in results:
        for segment in result.get("segments", []):
            for event in segment.get("events", []):
                event_counts[event] += 1
    
    event_distribution = dict(event_counts.most_common(10))
    
    # 4. Intent Distribution
    intent_counts = Counter()
    for result in results:
        for segment in result.get("segments", []):
            intent = segment.get("intent", "general_query")
            intent_counts[intent] += 1
    
    top_issues = dict(intent_counts.most_common(5))
    
    # 5. Priority Distribution
    priority_counts = Counter()
    for result in results:
        for segment in result.get("segments", []):
            priority = segment.get("priority", "low")
            priority_counts[priority] += 1
    
    priority_distribution = {
        "critical": priority_counts.get("critical", 0),
        "high": priority_counts.get("high", 0),
        "medium": priority_counts.get("medium", 0),
        "low": priority_counts.get("low", 0)
    }
    
    # 6. File Rankings (by importance score)
    file_rankings = []
    for result in results:
        segments = result.get("segments", [])
        
        # Calculate importance score
        complaint_count = sum(1 for s in segments if "complaint" in s.get("events", []))
        urgency_count = sum(1 for s in segments if "urgency" in s.get("events", []))
        escalation_count = sum(1 for s in segments if "escalation" in s.get("events", []))
        negative_count = sum(1 for s in segments if s.get("sentiment") == "negative")
        high_priority_count = sum(1 for s in segments if s.get("priority") in ["high", "critical"])
        risk_count = sum(1 for s in segments if len(s.get("risk_signals", [])) > 0)
        
        # Importance score formula
        score = (
            complaint_count * 2 +
            urgency_count * 3 +
            escalation_count * 4 +
            negative_count * 1.5 +
            high_priority_count * 2 +
            risk_count * 5
        )
        
        file_rankings.append({
            "file_id": result.get("file_id"),
            "file_name": result.get("file_name"),
            "score": round(score, 1),
            "segments": len(segments),
            "complaint_count": complaint_count,
            "urgency_count": urgency_count,
            "escalation_count": escalation_count,
            "negative_count": negative_count,
            "high_priority_count": high_priority_count,
            "risk_count": risk_count,
            "language": result.get("language", "en"),
            "summary": result.get("summary", {})
        })
    
    # Sort by score (highest first)
    file_rankings.sort(key=lambda x: x["score"], reverse=True)
    
    # 7. Language Distribution
    language_counts = Counter()
    for result in results:
        lang = result.get("language", "en")
        language_counts[lang] += 1
    
    language_distribution = dict(language_counts)
    
    # 8. Risk Analysis
    risk_signal_counts = Counter()
    for result in results:
        for segment in result.get("segments", []):
            for risk in segment.get("risk_signals", []):
                risk_signal_counts[risk] += 1
    
    risk_signals = dict(risk_signal_counts.most_common(5))
    
    # ============= BUILD RESPONSE =============
    insights = {
        "cluster_id": cluster_id,
        "cluster_name": cluster.get("name", "Unknown"),
        
        # Basic metrics
        "metrics": {
            "total_files": total_files,
            "total_segments": total_segments,
            "complaint_percentage": round((event_counts.get("complaint", 0) / total_segments * 100) if total_segments > 0 else 0, 1),
            "urgency_percentage": round((event_counts.get("urgency", 0) / total_segments * 100) if total_segments > 0 else 0, 1),
            "negative_percentage": sentiment_percentages.get("negative", 0),
            "high_priority_percentage": round(((priority_counts.get("high", 0) + priority_counts.get("critical", 0)) / total_segments * 100) if total_segments > 0 else 0, 1)
        },
        
        # Distributions
        "sentiment_distribution": sentiment_distribution,
        "sentiment_percentages": sentiment_percentages,
        "event_distribution": event_distribution,
        "priority_distribution": priority_distribution,
        "language_distribution": language_distribution,
        
        # Rankings
        "top_files": file_rankings[:10],  # Top 10 files
        "top_issues": top_issues,
        "risk_signals": risk_signals,
        
        # Additional insights
        "avg_segments_per_file": round(total_segments / total_files, 1) if total_files > 0 else 0,
        "files_with_risks": sum(1 for f in file_rankings if f["risk_count"] > 0),
        "files_with_escalation": sum(1 for f in file_rankings if f["escalation_count"] > 0)
    }
    
    return {"insights": insights}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/audio/{cluster_id}/{file_name}")
async def get_audio_file(cluster_id: str, file_name: str, user = Depends(get_current_user)):
    """Serve audio files for playback"""
    db = await get_db()
    user_id = str(user["_id"])
    
    from bson import ObjectId
    
    # Verify cluster ownership
    try:
        cluster_obj_id = ObjectId(cluster_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid cluster ID")
    
    cluster = await db.clusters.find_one({"_id": cluster_obj_id, "user_id": user_id})
    if not cluster:
        raise HTTPException(status_code=404, detail="Cluster not found")
    
    # Build file path
    file_path = UPLOAD_DIR / cluster_id / file_name
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    return FileResponse(
        path=str(file_path),
        media_type="audio/mpeg",
        filename=file_name
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
