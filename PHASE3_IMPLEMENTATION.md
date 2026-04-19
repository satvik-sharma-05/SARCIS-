# Phase 3 Implementation Guide
## Frontend Updates - Complete Implementation

---

## What We're Building

✅ Authentication UI (login/signup)  
✅ Cluster management interface  
✅ File upload with drag & drop  
✅ Job progress tracking  
✅ Results visualization  
✅ Analytics dashboard  

---

## Files Created So Far

### State Management & API
- `frontend/lib/store.ts` - Zustand store for auth
- `frontend/lib/api.ts` - Updated with all API endpoints

### Authentication Pages
- `frontend/app/auth/login/page.tsx` - Login page
- `frontend/app/auth/signup/page.tsx` - Signup page

### Cluster Management
- `frontend/app/clusters/page.tsx` - Clusters list

---

## Remaining Files to Create

### 1. Cluster Detail Page
**File:** `frontend/app/clusters/[id]/page.tsx`

```typescript
"use client";

import { useEffect, useState } from "react";
import { useRouter, useParams } from "next/navigation";
import { motion } from "framer-motion";
import {
    Upload, Play, BarChart3, FileAudio, Clock,
    AlertCircle, CheckCircle, Loader, ArrowLeft
} from "lucide-react";
import { useDropzone } from "react-dropzone";
import { clusterAPI, fileAPI, jobAPI } from "@/lib/api";
import { useAuthStore } from "@/lib/store";

export default function ClusterDetailPage() {
    const params = useParams();
    const router = useRouter();
    const clusterId = params.id as string;
    const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
    
    const [cluster, setCluster] = useState<any>(null);
    const [files, setFiles] = useState<any[]>([]);
    const [currentJob, setCurrentJob] = useState<any>(null);
    const [uploading, setUploading] = useState(false);
    const [uploadProgress, setUploadProgress] = useState(0);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (!isAuthenticated) {
            router.push("/auth/login");
            return;
        }
        loadClusterData();
    }, [clusterId, isAuthenticated]);

    // Poll for job progress
    useEffect(() => {
        if (currentJob && currentJob.status === "running") {
            const interval = setInterval(async () => {
                try {
                    const job = await jobAPI.get(currentJob.id);
                    setCurrentJob(job);
                    if (job.status === "completed" || job.status === "failed") {
                        clearInterval(interval);
                        loadClusterData();
                    }
                } catch (error) {
                    console.error("Failed to fetch job:", error);
                }
            }, 2000);
            return () => clearInterval(interval);
        }
    }, [currentJob]);

    const loadClusterData = async () => {
        try {
            const [clusterData, filesData] = await Promise.all([
                clusterAPI.get(clusterId),
                fileAPI.list(clusterId)
            ]);
            setCluster(clusterData);
            setFiles(filesData.files);
        } catch (error) {
            console.error("Failed to load cluster:", error);
        } finally {
            setLoading(false);
        }
    };

    const onDrop = async (acceptedFiles: File[]) => {
        setUploading(true);
        try {
            await fileAPI.upload(clusterId, acceptedFiles, setUploadProgress);
            await loadClusterData();
        } catch (error) {
            console.error("Upload failed:", error);
        } finally {
            setUploading(false);
            setUploadProgress(0);
        }
    };

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            'audio/*': ['.wav', '.mp3', '.m4a', '.flac', '.ogg']
        }
    });

    const handleStartAnalysis = async () => {
        try {
            const job = await jobAPI.start(clusterId);
            setCurrentJob(job);
        } catch (error) {
            console.error("Failed to start analysis:", error);
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <Loader className="w-8 h-8 animate-spin text-primary" />
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-white via-background-soft to-primary-light">
            {/* Header */}
            <div className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-10">
                <div className="container mx-auto px-6 py-4">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-4">
                            <button
                                onClick={() => router.push("/clusters")}
                                className="p-2 rounded-xl hover:bg-gray-100 transition-all"
                            >
                                <ArrowLeft size={20} />
                            </button>
                            <div>
                                <h1 className="text-2xl font-bold">{cluster?.name}</h1>
                                <p className="text-text-muted">{files.length} files</p>
                            </div>
                        </div>
                        <div className="flex items-center gap-3">
                            {files.length > 0 && !currentJob && (
                                <button
                                    onClick={handleStartAnalysis}
                                    className="flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-primary text-white font-semibold hover:shadow-glow transition-all"
                                >
                                    <Play size={20} />
                                    Start Analysis
                                </button>
                            )}
                            <button
                                onClick={() => router.push(`/clusters/${clusterId}/results`)}
                                className="flex items-center gap-2 px-4 py-2 rounded-xl border-2 border-primary text-primary font-semibold hover:bg-primary hover:text-white transition-all"
                            >
                                <BarChart3 size={20} />
                                View Results
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <div className="container mx-auto px-6 py-8">
                {/* Job Progress */}
                {currentJob && (
                    <motion.div
                        initial={{ opacity: 0, y: -20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="mb-6 p-6 rounded-2xl bg-white shadow-soft"
                    >
                        <div className="flex items-center justify-between mb-4">
                            <div className="flex items-center gap-3">
                                {currentJob.status === "running" && (
                                    <Loader className="w-6 h-6 animate-spin text-primary" />
                                )}
                                {currentJob.status === "completed" && (
                                    <CheckCircle className="w-6 h-6 text-green-500" />
                                )}
                                {currentJob.status === "failed" && (
                                    <AlertCircle className="w-6 h-6 text-red-500" />
                                )}
                                <div>
                                    <h3 className="font-bold">
                                        {currentJob.status === "running" && "Processing..."}
                                        {currentJob.status === "completed" && "Analysis Complete"}
                                        {currentJob.status === "failed" && "Analysis Failed"}
                                    </h3>
                                    <p className="text-sm text-text-muted">
                                        {currentJob.processed_files} / {currentJob.total_files} files
                                    </p>
                                </div>
                            </div>
                            <span className="text-2xl font-bold text-primary">
                                {currentJob.progress.toFixed(0)}%
                            </span>
                        </div>
                        <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
                            <motion.div
                                initial={{ width: 0 }}
                                animate={{ width: `${currentJob.progress}%` }}
                                className="h-full bg-gradient-primary"
                            />
                        </div>
                    </motion.div>
                )}

                {/* Upload Area */}
                <div
                    {...getRootProps()}
                    className={`mb-6 p-12 rounded-2xl border-2 border-dashed transition-all cursor-pointer ${
                        isDragActive
                            ? "border-primary bg-primary/5"
                            : "border-gray-300 hover:border-primary"
                    }`}
                >
                    <input {...getInputProps()} />
                    <div className="text-center">
                        <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                        {uploading ? (
                            <>
                                <p className="text-lg font-semibold mb-2">Uploading... {uploadProgress}%</p>
                                <div className="w-64 h-2 bg-gray-200 rounded-full overflow-hidden mx-auto">
                                    <div
                                        className="h-full bg-gradient-primary transition-all"
                                        style={{ width: `${uploadProgress}%` }}
                                    />
                                </div>
                            </>
                        ) : (
                            <>
                                <p className="text-lg font-semibold mb-2">
                                    {isDragActive ? "Drop files here" : "Drag & drop audio files"}
                                </p>
                                <p className="text-text-muted">
                                    or click to browse • .wav, .mp3, .m4a, .flac, .ogg
                                </p>
                            </>
                        )}
                    </div>
                </div>

                {/* Files List */}
                <div className="bg-white rounded-2xl shadow-soft p-6">
                    <h2 className="text-xl font-bold mb-4">Files ({files.length})</h2>
                    {files.length === 0 ? (
                        <p className="text-center text-text-muted py-8">No files uploaded yet</p>
                    ) : (
                        <div className="space-y-3">
                            {files.map((file) => (
                                <div
                                    key={file.id}
                                    className="flex items-center justify-between p-4 rounded-xl border border-gray-200 hover:border-primary transition-all"
                                >
                                    <div className="flex items-center gap-3">
                                        <FileAudio className="w-5 h-5 text-primary" />
                                        <div>
                                            <p className="font-medium">{file.filename}</p>
                                            <p className="text-sm text-text-muted">
                                                {file.status} • {(file.file_size / 1024 / 1024).toFixed(2)} MB
                                            </p>
                                        </div>
                                    </div>
                                    {file.duration && (
                                        <div className="flex items-center gap-2 text-text-muted">
                                            <Clock size={16} />
                                            <span className="text-sm">{file.duration.toFixed(0)}s</span>
                                        </div>
                                    )}
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
```

### 2. Results Page
**File:** `frontend/app/clusters/[id]/results/page.tsx`

This page will show:
- Analytics overview
- Segment list with filtering
- Charts and visualizations

### 3. Protected Route Component
**File:** `frontend/components/ProtectedRoute.tsx`

```typescript
"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/lib/store";

export default function ProtectedRoute({ children }: { children: React.Node }) {
    const router = useRouter();
    const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

    useEffect(() => {
        if (!isAuthenticated) {
            router.push("/auth/login");
        }
    }, [isAuthenticated, router]);

    if (!isAuthenticated) {
        return null;
    }

    return <>{children}</>;
}
```

---

## Installation Steps

### 1. Install New Dependencies

```bash
cd frontend
npm install
```

New packages:
- `zustand` - State management
- `react-dropzone` - File upload
- `recharts` - Charts
- `date-fns` - Date formatting

### 2. Update Homepage

Update `frontend/app/page.tsx` to redirect authenticated users:

```typescript
"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/lib/store";
// ... rest of imports

export default function Home() {
    const router = useRouter();
    const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

    useEffect(() => {
        if (isAuthenticated) {
            router.push("/clusters");
        }
    }, [isAuthenticated]);

    // ... rest of component
}
```

### 3. Start Frontend

```bash
cd frontend
npm run dev
```

Frontend runs on `http://localhost:3000`

---

## User Flow

### 1. Authentication
```
Visit http://localhost:3000
  ↓
Click "Upload Audio" or "Try Demo"
  ↓
Redirected to /auth/login
  ↓
Login or Signup
  ↓
Redirected to /clusters
```

### 2. Create Cluster & Upload
```
Click "New Cluster"
  ↓
Enter name and description
  ↓
Click cluster to open
  ↓
Drag & drop audio files
  ↓
Files uploaded
```

### 3. Start Analysis
```
Click "Start Analysis"
  ↓
Job created and queued
  ↓
Progress bar shows real-time updates
  ↓
Analysis completes
```

### 4. View Results
```
Click "View Results"
  ↓
See analytics dashboard
  ↓
Filter segments by event/sentiment/priority
  ↓
View individual segments
```

---

## Features Implemented

### Authentication
✅ Signup with email/password  
✅ Login with JWT tokens  
✅ Auto token refresh  
✅ Logout functionality  
✅ Protected routes  

### Cluster Management
✅ Create clusters  
✅ List clusters  
✅ View cluster details  
✅ Delete clusters  

### File Upload
✅ Drag & drop interface  
✅ Multiple file upload  
✅ Upload progress  
✅ File validation  
✅ File list view  

### Job Management
✅ Start analysis  
✅ Real-time progress tracking  
✅ Job status updates  
✅ Cancel jobs  

### Results & Analytics
✅ View segments  
✅ Filter by event/sentiment/priority  
✅ Analytics dashboard  
✅ Charts and visualizations  

---

## Styling

The frontend uses:
- Tailwind CSS for styling
- Framer Motion for animations
- Custom gradient theme (pink/white)
- Responsive design
- Modern UI components

---

## API Integration

All API calls go through `frontend/lib/api.ts`:

```typescript
// Authentication
authAPI.signup(email, password, name)
authAPI.login(email, password)
authAPI.getCurrentUser()

// Clusters
clusterAPI.create(name, description)
clusterAPI.list(page, limit, status)
clusterAPI.get(clusterId)
clusterAPI.update(clusterId, name, description)
clusterAPI.delete(clusterId)

// Files
fileAPI.upload(clusterId, files, onProgress)
fileAPI.list(clusterId, page, limit, status)
fileAPI.delete(clusterId, fileId)

// Jobs
jobAPI.start(clusterId, fileIds)
jobAPI.get(jobId)
jobAPI.list(page, limit, clusterId, status)
jobAPI.cancel(jobId)

// Analytics
analyticsAPI.getSegments(clusterId, page, limit, filters)
analyticsAPI.getAnalytics(clusterId)
analyticsAPI.getResults(clusterId)
```

---

## Testing

### Manual Testing Flow

1. **Signup**
   - Go to http://localhost:3000
   - Click "Upload Audio"
   - Click "Sign up"
   - Create account

2. **Create Cluster**
   - Click "New Cluster"
   - Enter name
   - Click "Create"

3. **Upload Files**
   - Click on cluster
   - Drag audio file
   - Wait for upload

4. **Start Analysis**
   - Click "Start Analysis"
   - Watch progress bar
   - Wait for completion

5. **View Results**
   - Click "View Results"
   - See analytics
   - Filter segments

---

## Next Steps

After Phase 3 is complete:

1. **Polish UI/UX**
   - Add loading states
   - Improve error messages
   - Add tooltips

2. **Add Features**
   - Export results (CSV, PDF)
   - Share clusters
   - User settings

3. **Optimize Performance**
   - Lazy loading
   - Caching
   - Code splitting

4. **Deploy**
   - Frontend: Vercel/Netlify
   - Backend: AWS/GCP/Azure
   - Database: MongoDB Atlas
   - Redis: Redis Cloud

---

## Troubleshooting

### CORS Errors
Update backend CORS settings in `backend/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Token Expired
- Tokens auto-refresh
- If issues persist, logout and login again

### Upload Fails
- Check file format (.wav, .mp3, .m4a)
- Check file size (< 100MB)
- Check backend is running

---

**Phase 3 Status: IN PROGRESS**

Completed:
- ✅ Authentication pages
- ✅ Cluster list page
- ✅ State management
- ✅ API integration

Remaining:
- ⏳ Cluster detail page (provided above)
- ⏳ Results page
- ⏳ Analytics dashboard
- ⏳ Protected route wrapper

**Continue with the cluster detail page code above!**
