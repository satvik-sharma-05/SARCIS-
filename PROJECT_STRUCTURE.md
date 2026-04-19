# 📁 SARCIS Project Structure

Complete overview of the project organization.

## Directory Tree

```
sarcis/
├── backend/                    # Python FastAPI backend
│   ├── main.py                # FastAPI application & endpoints
│   ├── audio_processor.py     # Whisper transcription
│   ├── nlp_engine.py          # NLP processing (sentiment, events, intent)
│   ├── genai_engine.py        # GenAI processing (Groq)
│   ├── utils/                 # Utility functions
│   │   ├── __init__.py
│   │   └── helpers.py         # File handling, cleanup
│   └── __init__.py
│
├── frontend/                   # Next.js React frontend
│   ├── app/                   # Next.js 14 app directory
│   │   ├── page.tsx           # Home/landing page
│   │   ├── layout.tsx         # Root layout
│   │   ├── globals.css        # Global styles
│   │   ├── upload/            # Upload page
│   │   │   └── page.tsx
│   │   ├── results/           # Results page
│   │   │   └── page.tsx
│   │   └── dashboard/         # Dashboard page
│   │       └── page.tsx
│   ├── lib/                   # Utility libraries
│   │   ├── api.ts             # API client
│   │   └── utils.ts           # Helper functions
│   ├── package.json           # Node dependencies
│   ├── tsconfig.json          # TypeScript config
│   ├── tailwind.config.ts     # Tailwind CSS config
│   ├── postcss.config.js      # PostCSS config
│   └── next.config.js         # Next.js config
│
├── test_audio/                # Test audio files directory
│   └── README.md              # Instructions for test files
│
├── .env                       # Environment variables
├── .gitignore                 # Git ignore rules
├── requirements.txt           # Python dependencies
├── package.json               # Root package.json (optional)
│
├── README.md                  # Main project documentation
├── SETUP.md                   # Detailed setup instructions
├── QUICKSTART.md              # Quick start guide
├── ARCHITECTURE.md            # System architecture
├── CONTRIBUTING.md            # Contribution guidelines
├── PROJECT_STRUCTURE.md       # This file
├── LICENSE                    # MIT License
│
├── start.sh                   # Linux/Mac startup script
└── start.bat                  # Windows startup script
```

## File Descriptions

### Backend Files

#### `backend/main.py`
- FastAPI application setup
- API endpoints definition
- CORS configuration
- Request/response handling
- Error handling

**Key Endpoints:**
- `GET /` - API information
- `GET /health` - Health check
- `POST /api/analyze` - Multi-file analysis
- `POST /api/analyze-single` - Single file analysis

#### `backend/audio_processor.py`
- OpenAI Whisper integration
- Audio transcription
- Timestamp extraction
- Language detection
- Audio metadata extraction

**Key Methods:**
- `transcribe(audio_path)` - Main transcription
- `get_audio_info(audio_path)` - Get metadata

#### `backend/nlp_engine.py`
- HuggingFace Transformers integration
- Sentiment analysis
- Event detection (keyword-based)
- Intent classification
- Language translation
- Priority assignment

**Key Methods:**
- `process_segments()` - Batch NLP processing
- `detect_events()` - Multi-label classification
- `analyze_sentiment()` - Sentiment scoring
- `classify_intent()` - Intent detection
- `assign_priorities()` - Priority logic

#### `backend/genai_engine.py`
- Groq API integration
- Selective GenAI processing
- Refined event classification
- Priority refinement
- Explanation generation

**Key Methods:**
- `should_process_with_genai()` - Filter logic
- `analyze_segment_batch()` - Batch GenAI calls
- `process_high_priority_segments()` - Main pipeline

#### `backend/utils/helpers.py`
- File upload handling
- Temporary file management
- Cleanup utilities
- Time formatting

### Frontend Files

#### `frontend/app/page.tsx`
- Landing page
- Hero section
- Features showcase
- How it works
- Call-to-action

#### `frontend/app/upload/page.tsx`
- File upload interface
- Drag & drop functionality
- File preview
- Upload progress
- API integration

#### `frontend/app/results/page.tsx`
- Analysis results display
- Segment timeline
- Event tags
- Priority badges
- Interactive segments

#### `frontend/app/dashboard/page.tsx`
- Main dashboard
- Quick actions
- Navigation cards

#### `frontend/lib/api.ts`
- Axios configuration
- API client setup
- Request helpers
- Error handling

#### `frontend/lib/utils.ts`
- Utility functions
- Time formatting
- File size formatting
- Color helpers
- Class name merging

#### `frontend/tailwind.config.ts`
- Tailwind CSS configuration
- Custom colors (pink theme)
- Custom animations
- Shadow utilities
- Gradient definitions

### Configuration Files

#### `.env`
- Environment variables
- API keys
- Model configurations
- Feature flags

#### `requirements.txt`
- Python dependencies
- Version specifications
- Backend packages

#### `frontend/package.json`
- Node.js dependencies
- Scripts
- Frontend packages

#### `.gitignore`
- Ignored files/folders
- Temp files
- Environment files
- Build artifacts

### Documentation Files

#### `README.md`
- Project overview
- Quick introduction
- Key features
- Tech stack
- Basic usage

#### `SETUP.md`
- Detailed installation
- Prerequisites
- Step-by-step setup
- Troubleshooting
- Production deployment

#### `QUICKSTART.md`
- Fast setup guide
- Essential steps only
- Common issues
- Quick tips

#### `ARCHITECTURE.md`
- System design
- Component details
- Data flow
- API specifications
- Scaling strategies

#### `CONTRIBUTING.md`
- Contribution guidelines
- Code style
- PR process
- Issue reporting

#### `LICENSE`
- MIT License
- Usage terms
- Copyright information

### Scripts

#### `start.sh` (Linux/Mac)
- Automated startup
- Backend + Frontend
- Process management

#### `start.bat` (Windows)
- Automated startup
- Backend + Frontend
- Process management

## Key Directories

### `/backend`
All Python backend code. Self-contained FastAPI application.

### `/frontend`
Complete Next.js application with app router.

### `/test_audio`
Place test audio files here. Ignored by git.

### `/backend/utils`
Shared utility functions for backend.

### `/frontend/lib`
Shared utility functions for frontend.

### `/frontend/app`
Next.js 14 app directory structure.

## Generated Directories (Not in Git)

### `backend/temp_uploads/`
Temporary storage for uploaded audio files. Auto-created and cleaned.

### `frontend/node_modules/`
Node.js dependencies. Created by `npm install`.

### `frontend/.next/`
Next.js build output. Created by `npm run build`.

### `__pycache__/`
Python bytecode cache. Auto-generated.

## File Naming Conventions

### Python Files
- `snake_case.py`
- Descriptive names
- Module-level files

### TypeScript/React Files
- `PascalCase.tsx` for components
- `camelCase.ts` for utilities
- `kebab-case/` for directories

### Configuration Files
- `lowercase.config.js`
- `.dotfiles` for environment

## Import Structure

### Backend Imports
```python
from audio_processor import AudioProcessor
from nlp_engine import NLPEngine
from genai_engine import GenAIEngine
from utils.helpers import save_upload_file
```

### Frontend Imports
```typescript
import { api } from "@/lib/api";
import { cn, formatTime } from "@/lib/utils";
```

## Build Artifacts

### Backend
- `__pycache__/` - Python cache
- `*.pyc` - Compiled Python
- `temp_uploads/` - Temp files

### Frontend
- `.next/` - Build output
- `out/` - Static export
- `node_modules/` - Dependencies

## Environment Files

- `.env` - Main environment (not in git)
- `.env.example` - Template (in git)
- `.env.local` - Local overrides (not in git)

## Data Flow Through Files

```
User Upload
    ↓
frontend/app/upload/page.tsx
    ↓
frontend/lib/api.ts
    ↓
backend/main.py (POST /api/analyze)
    ↓
backend/audio_processor.py (Whisper)
    ↓
backend/nlp_engine.py (NLP)
    ↓
backend/genai_engine.py (GenAI)
    ↓
backend/main.py (Response)
    ↓
frontend/app/results/page.tsx
```

## Module Dependencies

### Backend Dependencies
```
main.py
├── audio_processor.py
├── nlp_engine.py
├── genai_engine.py
└── utils/helpers.py
```

### Frontend Dependencies
```
app/page.tsx
├── lib/api.ts
└── lib/utils.ts

app/upload/page.tsx
├── lib/api.ts
└── lib/utils.ts

app/results/page.tsx
└── lib/utils.ts
```

## Size Estimates

- Backend code: ~5 KB
- Frontend code: ~15 KB
- Dependencies (Python): ~2 GB
- Dependencies (Node): ~500 MB
- Whisper model (base): ~140 MB
- NLP models: ~500 MB

## Development Workflow

1. Edit backend: `backend/*.py`
2. Test API: `http://localhost:8000/docs`
3. Edit frontend: `frontend/app/**/*.tsx`
4. Test UI: `http://localhost:3000`
5. Commit changes
6. Push to repository

## Production Structure

```
Production/
├── backend/ (Deployed to cloud server)
│   └── Gunicorn + FastAPI
├── frontend/ (Deployed to Vercel/Netlify)
│   └── Static Next.js build
└── .env (Environment variables in hosting platform)
```
