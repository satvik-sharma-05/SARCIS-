# 🔌 SARCIP API Specification
## Complete REST API Documentation

**Base URL:** `https://api.sarcip.com` (Production)  
**Base URL:** `http://localhost:8000` (Development)

**Version:** 2.0.0  
**Authentication:** JWT Bearer Token

---

## 📋 Table of Contents

1. [Authentication](#authentication)
2. [Users](#users)
3. [Clusters](#clusters)
4. [Files](#files)
5. [Jobs](#jobs)
6. [Segments](#segments)
7. [Analytics](#analytics)
8. [Health](#health)

---

## 🔐 Authentication

### POST /api/auth/signup
Create a new user account.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "name": "John Doe"
}
```

**Response:** `201 Created`
```json
{
  "user": {
    "id": "507f1f77bcf86cd799439011",
    "email": "user@example.com",
    "name": "John Doe",
    "created_at": "2024-01-15T10:30:00Z"
  },
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

**Errors:**
- `400` - Invalid email format
- `409` - Email already exists

---

### POST /api/auth/login
Authenticate user and get tokens.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response:** `200 OK`
```json
{
  "user": {
    "id": "507f1f77bcf86cd799439011",
    "email": "user@example.com",
    "name": "John Doe"
  },
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

**Errors:**
- `401` - Invalid credentials

---

### POST /api/auth/refresh
Refresh access token using refresh token.

**Request:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

---

### GET /api/auth/me
Get current user profile.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
{
  "id": "507f1f77bcf86cd799439011",
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2024-01-15T10:30:00Z",
  "last_login": "2024-01-20T14:22:00Z",
  "cluster_count": 5,
  "total_files_processed": 1250
}
```

---

## 👥 Users

### PUT /api/users/me
Update current user profile.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request:**
```json
{
  "name": "John Smith",
  "email": "newmail@example.com"
}
```

**Response:** `200 OK`
```json
{
  "id": "507f1f77bcf86cd799439011",
  "email": "newmail@example.com",
  "name": "John Smith",
  "updated_at": "2024-01-20T15:00:00Z"
}
```

---

### POST /api/users/me/change-password
Change user password.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request:**
```json
{
  "current_password": "OldPass123!",
  "new_password": "NewPass456!"
}
```

**Response:** `200 OK`
```json
{
  "message": "Password updated successfully"
}
```

---

## 📁 Clusters

### POST /api/clusters
Create a new cluster.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request:**
```json
{
  "name": "Customer Support Calls - Q1 2024",
  "description": "Analysis of customer support calls from January to March 2024"
}
```

**Response:** `201 Created`
```json
{
  "id": "65a1b2c3d4e5f6789abcdef0",
  "user_id": "507f1f77bcf86cd799439011",
  "name": "Customer Support Calls - Q1 2024",
  "description": "Analysis of customer support calls from January to March 2024",
  "file_count": 0,
  "status": "active",
  "created_at": "2024-01-20T10:00:00Z",
  "updated_at": "2024-01-20T10:00:00Z",
  "last_processed": null
}
```

---

### GET /api/clusters
List all clusters for current user.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `page` (int, default: 1) - Page number
- `limit` (int, default: 20) - Items per page
- `status` (string, optional) - Filter by status: active, processing, completed
- `sort` (string, default: -created_at) - Sort field

**Response:** `200 OK`
```json
{
  "clusters": [
    {
      "id": "65a1b2c3d4e5f6789abcdef0",
      "name": "Customer Support Calls - Q1 2024",
      "description": "Analysis of customer support calls",
      "file_count": 150,
      "status": "completed",
      "created_at": "2024-01-20T10:00:00Z",
      "last_processed": "2024-01-20T15:30:00Z",
      "summary": {
        "total_segments": 3750,
        "critical_count": 25,
        "high_count": 180,
        "complaint_percentage": 32.5
      }
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 5,
    "pages": 1
  }
}
```

---

### GET /api/clusters/{cluster_id}
Get cluster details.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
{
  "id": "65a1b2c3d4e5f6789abcdef0",
  "user_id": "507f1f77bcf86cd799439011",
  "name": "Customer Support Calls - Q1 2024",
  "description": "Analysis of customer support calls",
  "file_count": 150,
  "status": "completed",
  "created_at": "2024-01-20T10:00:00Z",
  "updated_at": "2024-01-20T15:30:00Z",
  "last_processed": "2024-01-20T15:30:00Z",
  "processing_stats": {
    "total_duration": 7500.5,
    "avg_file_duration": 50.0,
    "total_segments": 3750,
    "languages_detected": ["en", "hi", "es"]
  }
}
```

**Errors:**
- `404` - Cluster not found
- `403` - Not authorized to access this cluster

---

### PUT /api/clusters/{cluster_id}
Update cluster details.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request:**
```json
{
  "name": "Customer Support Calls - Q1 2024 (Updated)",
  "description": "Updated description"
}
```

**Response:** `200 OK`
```json
{
  "id": "65a1b2c3d4e5f6789abcdef0",
  "name": "Customer Support Calls - Q1 2024 (Updated)",
  "description": "Updated description",
  "updated_at": "2024-01-21T09:00:00Z"
}
```

---

### DELETE /api/clusters/{cluster_id}
Delete a cluster and all associated files.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `204 No Content`

**Errors:**
- `404` - Cluster not found
- `403` - Not authorized
- `409` - Cluster is currently processing

---

## 📄 Files

### POST /api/clusters/{cluster_id}/upload
Upload audio files to a cluster.

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
```

**Request:**
```
files: [File, File, File, ...]
```

**Response:** `201 Created`
```json
{
  "cluster_id": "65a1b2c3d4e5f6789abcdef0",
  "uploaded_files": [
    {
      "id": "65a1b2c3d4e5f6789abcdef1",
      "filename": "call_001.wav",
      "file_size": 2048576,
      "status": "uploaded",
      "uploaded_at": "2024-01-20T11:00:00Z"
    },
    {
      "id": "65a1b2c3d4e5f6789abcdef2",
      "filename": "call_002.mp3",
      "file_size": 1536000,
      "status": "uploaded",
      "uploaded_at": "2024-01-20T11:00:01Z"
    }
  ],
  "total_uploaded": 2,
  "failed": []
}
```

**Errors:**
- `400` - Invalid file format
- `413` - File too large (max 100MB per file)
- `429` - Too many files (max 1000 per upload)

---

### GET /api/clusters/{cluster_id}/files
List files in a cluster.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `page` (int, default: 1)
- `limit` (int, default: 50)
- `status` (string, optional) - Filter by status
- `sort` (string, default: -uploaded_at)

**Response:** `200 OK`
```json
{
  "files": [
    {
      "id": "65a1b2c3d4e5f6789abcdef1",
      "cluster_id": "65a1b2c3d4e5f6789abcdef0",
      "filename": "call_001.wav",
      "file_size": 2048576,
      "duration": 45.5,
      "language": "en",
      "status": "completed",
      "uploaded_at": "2024-01-20T11:00:00Z",
      "processed_at": "2024-01-20T11:05:30Z",
      "segment_count": 25,
      "summary": {
        "critical_segments": 2,
        "high_priority_segments": 5,
        "negative_sentiment_count": 8
      }
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 50,
    "total": 150,
    "pages": 3
  }
}
```

---

### GET /api/files/{file_id}
Get file details.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
{
  "id": "65a1b2c3d4e5f6789abcdef1",
  "cluster_id": "65a1b2c3d4e5f6789abcdef0",
  "filename": "call_001.wav",
  "file_size": 2048576,
  "duration": 45.5,
  "language": "en",
  "status": "completed",
  "uploaded_at": "2024-01-20T11:00:00Z",
  "processed_at": "2024-01-20T11:05:30Z",
  "segment_count": 25,
  "file_path": "uploads/65a1b2c3d4e5f6789abcdef0/65a1b2c3d4e5f6789abcdef1.wav"
}
```

---

### GET /api/files/{file_id}/audio
Stream audio file.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```
Content-Type: audio/wav
Content-Length: 2048576
[Binary audio data]
```

---

### DELETE /api/files/{file_id}
Delete a file from cluster.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `204 No Content`

---

## ⚙️ Jobs

### POST /api/clusters/{cluster_id}/analyze
Start analysis job for a cluster.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request:**
```json
{
  "file_ids": ["65a1b2c3d4e5f6789abcdef1", "65a1b2c3d4e5f6789abcdef2"],
  "options": {
    "enable_genai": true,
    "whisper_model": "base",
    "batch_size": 5
  }
}
```

**Response:** `202 Accepted`
```json
{
  "job_id": "65a1b2c3d4e5f6789abcdef3",
  "cluster_id": "65a1b2c3d4e5f6789abcdef0",
  "status": "pending",
  "total_files": 2,
  "created_at": "2024-01-20T11:10:00Z",
  "estimated_completion": "2024-01-20T11:15:00Z"
}
```

---

### GET /api/jobs/{job_id}
Get job status and progress.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
{
  "id": "65a1b2c3d4e5f6789abcdef3",
  "cluster_id": "65a1b2c3d4e5f6789abcdef0",
  "user_id": "507f1f77bcf86cd799439011",
  "status": "running",
  "total_files": 150,
  "processed_files": 75,
  "progress": 50.0,
  "created_at": "2024-01-20T11:10:00Z",
  "started_at": "2024-01-20T11:10:05Z",
  "estimated_completion": "2024-01-20T11:25:00Z",
  "current_file": "call_075.wav",
  "errors": []
}
```

**Status Values:**
- `pending` - Job created, waiting to start
- `running` - Currently processing
- `completed` - Successfully completed
- `failed` - Job failed
- `cancelled` - User cancelled

---

### POST /api/jobs/{job_id}/cancel
Cancel a running job.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
{
  "job_id": "65a1b2c3d4e5f6789abcdef3",
  "status": "cancelled",
  "processed_files": 75,
  "cancelled_at": "2024-01-20T11:15:00Z"
}
```

---

### GET /api/jobs
List jobs for current user.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `cluster_id` (string, optional) - Filter by cluster
- `status` (string, optional) - Filter by status
- `page` (int, default: 1)
- `limit` (int, default: 20)

**Response:** `200 OK`
```json
{
  "jobs": [
    {
      "id": "65a1b2c3d4e5f6789abcdef3",
      "cluster_id": "65a1b2c3d4e5f6789abcdef0",
      "cluster_name": "Customer Support Calls - Q1 2024",
      "status": "completed",
      "total_files": 150,
      "processed_files": 150,
      "progress": 100.0,
      "created_at": "2024-01-20T11:10:00Z",
      "completed_at": "2024-01-20T11:30:00Z",
      "duration": 1200
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 10,
    "pages": 1
  }
}
```

---

## 📊 Segments

### GET /api/clusters/{cluster_id}/segments
Get segments from a cluster with filtering.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `file_id` (string, optional) - Filter by file
- `event` (string, optional) - Filter by event type
- `sentiment` (string, optional) - Filter by sentiment
- `priority` (string, optional) - Filter by priority
- `min_confidence` (float, optional) - Minimum confidence score
- `page` (int, default: 1)
- `limit` (int, default: 50)
- `sort` (string, default: -priority)

**Response:** `200 OK`
```json
{
  "segments": [
    {
      "id": "65a1b2c3d4e5f6789abcdef4",
      "file_id": "65a1b2c3d4e5f6789abcdef1",
      "cluster_id": "65a1b2c3d4e5f6789abcdef0",
      "filename": "call_001.wav",
      "start": 10.2,
      "end": 14.5,
      "text": "I've been trying to access my account for hours",
      "translated_text": "I've been trying to access my account for hours",
      "events": ["complaint", "urgency"],
      "sentiment": "negative",
      "intent": "account_access",
      "priority": "high",
      "confidence": 0.87,
      "genai_explanation": "Customer expressing urgent account access issue with frustration"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 50,
    "total": 1200,
    "pages": 24
  },
  "filters_applied": {
    "event": "complaint",
    "priority": "high"
  }
}
```

---

### GET /api/segments/{segment_id}
Get detailed segment information.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
{
  "id": "65a1b2c3d4e5f6789abcdef4",
  "file_id": "65a1b2c3d4e5f6789abcdef1",
  "cluster_id": "65a1b2c3d4e5f6789abcdef0",
  "filename": "call_001.wav",
  "start": 10.2,
  "end": 14.5,
  "duration": 4.3,
  "text": "I've been trying to access my account for hours",
  "translated_text": "I've been trying to access my account for hours",
  "was_translated": false,
  "language": "en",
  "events": ["complaint", "urgency"],
  "sentiment": "negative",
  "sentiment_confidence": 0.92,
  "intent": "account_access",
  "intent_confidence": 0.85,
  "priority": "high",
  "confidence": 0.87,
  "genai_processed": true,
  "genai_explanation": "Customer expressing urgent account access issue with frustration",
  "context": {
    "previous_segment": {
      "text": "Hello, I need help",
      "sentiment": "neutral"
    },
    "next_segment": {
      "text": "This is really frustrating",
      "sentiment": "negative"
    }
  }
}
```

---

## 📈 Analytics

### GET /api/clusters/{cluster_id}/analytics
Get aggregated analytics for a cluster.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
{
  "cluster_id": "65a1b2c3d4e5f6789abcdef0",
  "cluster_name": "Customer Support Calls - Q1 2024",
  "generated_at": "2024-01-20T12:00:00Z",
  
  "overview": {
    "total_files": 150,
    "total_segments": 3750,
    "total_duration": 7500.5,
    "avg_file_duration": 50.0,
    "languages": {
      "en": 120,
      "hi": 20,
      "es": 10
    }
  },
  
  "events": {
    "complaint": {
      "count": 1200,
      "percentage": 32.0
    },
    "urgency": {
      "count": 800,
      "percentage": 21.3
    },
    "fraud_risk": {
      "count": 50,
      "percentage": 1.3
    },
    "legal_escalation": {
      "count": 20,
      "percentage": 0.5
    },
    "abuse": {
      "count": 30,
      "percentage": 0.8
    },
    "high_risk_security": {
      "count": 40,
      "percentage": 1.1
    },
    "request": {
      "count": 1500,
      "percentage": 40.0
    },
    "neutral": {
      "count": 1110,
      "percentage": 29.6
    }
  },
  
  "sentiment": {
    "positive": {
      "count": 750,
      "percentage": 20.0
    },
    "negative": {
      "count": 1500,
      "percentage": 40.0
    },
    "neutral": {
      "count": 1500,
      "percentage": 40.0
    }
  },
  
  "priority": {
    "critical": {
      "count": 75,
      "percentage": 2.0
    },
    "high": {
      "count": 450,
      "percentage": 12.0
    },
    "medium": {
      "count": 1125,
      "percentage": 30.0
    },
    "low": {
      "count": 2100,
      "percentage": 56.0
    }
  },
  
  "intents": [
    {
      "intent": "technical_issue",
      "count": 1200,
      "percentage": 32.0
    },
    {
      "intent": "billing",
      "count": 900,
      "percentage": 24.0
    },
    {
      "intent": "account_access",
      "count": 750,
      "percentage": 20.0
    },
    {
      "intent": "feature_request",
      "count": 450,
      "percentage": 12.0
    },
    {
      "intent": "general_query",
      "count": 450,
      "percentage": 12.0
    }
  ],
  
  "trends": {
    "daily": [
      {
        "date": "2024-01-15",
        "files_processed": 30,
        "complaints": 240,
        "urgency": 160,
        "negative_sentiment": 300
      }
    ],
    "hourly": [
      {
        "hour": 9,
        "complaints": 50,
        "urgency": 30
      }
    ]
  },
  
  "top_issues": [
    {
      "issue": "Account access problems",
      "count": 450,
      "avg_priority": "high",
      "sample_segments": ["65a1b2c3d4e5f6789abcdef4"]
    }
  ]
}
```

---

### GET /api/analytics/dashboard
Get user-level dashboard analytics.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
{
  "user_id": "507f1f77bcf86cd799439011",
  "total_clusters": 5,
  "total_files": 750,
  "total_segments": 18750,
  "total_processing_time": 37500.0,
  
  "recent_activity": [
    {
      "type": "cluster_created",
      "cluster_name": "New Cluster",
      "timestamp": "2024-01-20T10:00:00Z"
    },
    {
      "type": "job_completed",
      "cluster_name": "Customer Support Calls",
      "files_processed": 150,
      "timestamp": "2024-01-20T11:30:00Z"
    }
  ],
  
  "top_clusters": [
    {
      "id": "65a1b2c3d4e5f6789abcdef0",
      "name": "Customer Support Calls - Q1 2024",
      "file_count": 150,
      "critical_segments": 75
    }
  ]
}
```

---

## 🏥 Health

### GET /health
Check API health status.

**Response:** `200 OK`
```json
{
  "status": "healthy",
  "timestamp": "2024-01-20T12:00:00Z",
  "version": "2.0.0",
  "services": {
    "database": "connected",
    "redis": "connected",
    "storage": "available",
    "whisper": "loaded",
    "nlp": "loaded",
    "genai": "enabled"
  },
  "workers": {
    "active": 5,
    "idle": 3,
    "busy": 2
  }
}
```

---

### GET /metrics
Get system metrics (admin only).

**Headers:**
```
Authorization: Bearer <admin_access_token>
```

**Response:** `200 OK`
```json
{
  "requests": {
    "total": 125000,
    "success": 123500,
    "errors": 1500,
    "avg_response_time": 185
  },
  "processing": {
    "files_processed_today": 1500,
    "avg_processing_time": 28.5,
    "queue_length": 25
  },
  "storage": {
    "total_files": 50000,
    "total_size_gb": 250.5
  }
}
```

---

## 🔒 Authentication Flow

### Standard Flow
```
1. POST /api/auth/signup or /api/auth/login
   → Receive access_token + refresh_token

2. Include in all requests:
   Authorization: Bearer <access_token>

3. When access_token expires (30 min):
   POST /api/auth/refresh
   → Receive new access_token

4. Continue using new access_token
```

---

## 📊 Rate Limits

| Endpoint | Rate Limit |
|----------|------------|
| Auth endpoints | 10 req/min |
| Upload | 100 files/hour |
| Analysis | 10 jobs/hour |
| Read operations | 1000 req/hour |

---

## 🚨 Error Responses

### Standard Error Format
```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Invalid file format",
    "details": {
      "field": "files",
      "allowed_formats": [".wav", ".mp3", ".m4a"]
    },
    "timestamp": "2024-01-20T12:00:00Z",
    "request_id": "req_abc123"
  }
}
```

### Error Codes
- `INVALID_REQUEST` - 400
- `UNAUTHORIZED` - 401
- `FORBIDDEN` - 403
- `NOT_FOUND` - 404
- `CONFLICT` - 409
- `RATE_LIMIT_EXCEEDED` - 429
- `INTERNAL_ERROR` - 500
- `SERVICE_UNAVAILABLE` - 503

---

## 📝 Notes

1. All timestamps are in ISO 8601 format (UTC)
2. All IDs are MongoDB ObjectId strings
3. File sizes are in bytes
4. Durations are in seconds
5. Percentages are 0-100
6. Confidence scores are 0-1

---

## 🔄 Pagination

All list endpoints support pagination:

**Query Parameters:**
- `page` - Page number (1-indexed)
- `limit` - Items per page (max 100)

**Response:**
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "pages": 8,
    "has_next": true,
    "has_prev": false
  }
}
```

---

## 🔍 Filtering & Sorting

**Filtering:**
```
GET /api/clusters/123/segments?event=complaint&priority=high
```

**Sorting:**
```
GET /api/clusters?sort=-created_at  # Descending
GET /api/clusters?sort=name          # Ascending
```

---

## 📦 Batch Operations

### Batch Delete Files
```
DELETE /api/files/batch
Body: { "file_ids": ["id1", "id2", "id3"] }
```

### Batch Update Segments
```
PATCH /api/segments/batch
Body: { "segment_ids": ["id1", "id2"], "updates": { "priority": "high" } }
```

---

**End of API Specification**
