"""Data models"""
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


class User(BaseModel):
    id: str
    email: EmailStr
    name: str
    created_at: datetime


class Cluster(BaseModel):
    id: str
    user_id: str
    name: str
    created_at: datetime
    status: str
    file_count: int = 0


class FileRecord(BaseModel):
    id: str
    cluster_id: str
    file_name: str
    file_path: str
    uploaded_at: datetime
    status: str


class Segment(BaseModel):
    start: float
    end: float
    text: str
    events: List[str]
    sentiment: str
    priority: str


class Result(BaseModel):
    id: str
    cluster_id: str
    file_id: str
    file_name: str
    segments: List[Segment]
