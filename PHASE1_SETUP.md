# Phase 1 Setup Guide

## What We've Built

✅ MongoDB database layer with repositories  
✅ JWT authentication system  
✅ User signup/login/refresh endpoints  
✅ Cluster CRUD operations  
✅ File upload to clusters  
✅ Protected routes with authentication  

## Installation Steps

### 1. Install New Dependencies

```bash
cd backend
pip install -r requirements.txt
```

New packages added:
- `motor` - Async MongoDB driver
- `pymongo` - MongoDB driver
- `pydantic` - Data validation
- `python-jose[cryptography]` - JWT tokens
- `passlib[bcrypt]` - Password hashing

### 2. Update Environment Variables

Your `.env` file has been updated with:
```env
MONGODB_DB_NAME=sarcip
JWT_SECRET_KEY=your-secret-key-change-this-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

**IMPORTANT:** Generate a secure JWT secret key:
```bash
# On Linux/Mac
openssl rand -hex 32

# On Windows (PowerShell)
python -c "import secrets; print(secrets.token_hex(32))"
```

Replace `JWT_SECRET_KEY` in `.env` with the generated key.

### 3. Start MongoDB

If you don't have MongoDB running, start it with Docker:

```bash
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

Or use your existing MongoDB Atlas connection (already in .env).

### 4. Start the Backend

```bash
cd backend
python main.py
```

The server will start on `http://localhost:8000`

### 5. Test the API

Open your browser and go to:
```
http://localhost:8000/docs
```

You'll see the interactive API documentation (Swagger UI).

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Create account
- `POST /api/auth/login` - Login
- `POST /api/auth/refresh` - Refresh token
- `GET /api/auth/me` - Get current user

### Clusters
- `POST /api/clusters` - Create cluster
- `GET /api/clusters` - List clusters
- `GET /api/clusters/{id}` - Get cluster details
- `PUT /api/clusters/{id}` - Update cluster
- `DELETE /api/clusters/{id}` - Delete cluster

### Files
- `POST /api/clusters/{id}/upload` - Upload files
- `GET /api/clusters/{id}/files` - List files
- `DELETE /api/clusters/{id}/files/{file_id}` - Delete file

## Testing the Flow

### 1. Create an Account

```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!",
    "name": "Test User"
  }'
```

Response:
```json
{
  "user": {
    "id": "...",
    "email": "test@example.com",
    "name": "Test User"
  },
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

Save the `access_token` for next requests.

### 2. Create a Cluster

```bash
curl -X POST http://localhost:8000/api/clusters \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "name": "Customer Support Calls Q1",
    "description": "Analysis of Q1 support calls"
  }'
```

Response:
```json
{
  "id": "...",
  "name": "Customer Support Calls Q1",
  "file_count": 0,
  "status": "active"
}
```

### 3. Upload Files

```bash
curl -X POST http://localhost:8000/api/clusters/CLUSTER_ID/upload \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "files=@audio1.wav" \
  -F "files=@audio2.mp3"
```

### 4. List Clusters

```bash
curl -X GET http://localhost:8000/api/clusters \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Database Structure

MongoDB collections created:
- `users` - User accounts
- `clusters` - Audio file clusters
- `files` - Individual audio files
- `segments` - Transcription segments
- `jobs` - Processing jobs

## File Storage

Uploaded files are stored in:
```
backend/uploads/{cluster_id}/{file_id}.wav
```

## What's Next (Phase 2)

- [ ] Job queue system (Redis + Celery)
- [ ] Worker processes for audio analysis
- [ ] Progress tracking
- [ ] Integrate existing audio processing pipeline
- [ ] Real-time updates

## Troubleshooting

### MongoDB Connection Error
```
Failed to connect to MongoDB
```
**Solution:** Check your `MONGO_URI` in `.env` or start MongoDB locally.

### Import Errors
```
ModuleNotFoundError: No module named 'motor'
```
**Solution:** Run `pip install -r requirements.txt`

### JWT Token Invalid
```
Could not validate credentials
```
**Solution:** Make sure you're including the token in the header:
```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### File Upload Fails
```
Invalid file format
```
**Solution:** Only `.wav`, `.mp3`, `.m4a`, `.flac`, `.ogg` files are allowed.

## Testing with Swagger UI

1. Go to `http://localhost:8000/docs`
2. Click on `/api/auth/signup`
3. Click "Try it out"
4. Fill in the request body
5. Click "Execute"
6. Copy the `access_token` from the response
7. Click the "Authorize" button at the top
8. Paste the token (without "Bearer")
9. Now you can test all protected endpoints!

## Verification Checklist

- [ ] Backend starts without errors
- [ ] Can access `/docs` endpoint
- [ ] Can create a user account
- [ ] Can login and receive tokens
- [ ] Can create a cluster
- [ ] Can upload files to cluster
- [ ] Can list clusters
- [ ] MongoDB shows data in collections

## Next Steps

Once Phase 1 is working, we'll move to Phase 2:
1. Set up Redis for job queue
2. Create Celery workers
3. Integrate audio processing pipeline
4. Add progress tracking
5. Update frontend with authentication

---

**Phase 1 Complete!** 🎉

You now have:
- User authentication
- Cluster management
- File uploads
- Database persistence
- Protected API endpoints
