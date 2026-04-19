# 📡 SARCIS API Documentation

Complete API reference for the SARCIS backend.

## Base URL

```
Development: http://localhost:8000
Production: https://api.yourdomain.com
```

## Authentication

Currently, the API does not require authentication. For production, implement JWT tokens or API keys.

## Endpoints

### 1. Root Endpoint

Get API information.

**Endpoint:** `GET /`

**Response:**
```json
{
  "message": "SARCIS API",
  "version": "1.0.0",
  "status": "running"
}
```

**Example:**
```bash
curl http://localhost:8000/
```

---

### 2. Health Check

Check API health and model status.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "whisper_loaded": true,
  "nlp_loaded": true,
  "genai_enabled": true
}
```

**Status Codes:**
- `200 OK` - Service is healthy
- `503 Service Unavailable` - Service is down

**Example:**
```bash
curl http://localhost:8000/health
```

---

### 3. Analyze Multiple Audio Files

Analyze multiple audio files and return structured insights.

**Endpoint:** `POST /api/analyze`

**Content-Type:** `multipart/form-data`

**Parameters:**
- `files` (required): Array of audio files
  - Supported formats: `.wav`, `.mp3`, `.m4a`
  - Max files: 50 (configurable)
  - Max size per file: 100MB (recommended)

**Request Example (cURL):**
```bash
curl -X POST http://localhost:8000/api/analyze \
  -F "files=@audio1.wav" \
  -F "files=@audio2.mp3" \
  -F "files=@audio3.m4a"
```

**Request Example (JavaScript):**
```javascript
const formData = new FormData();
formData.append('files', file1);
formData.append('files', file2);

const response = await fetch('http://localhost:8000/api