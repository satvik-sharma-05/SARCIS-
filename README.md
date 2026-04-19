# SARCIS - Smart Audio Risk & Context Intelligence System

> An AI-powered audio analysis platform that extracts deep insights from customer service call recordings using advanced speech recognition, translation, and LLM-based intelligence.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Next.js](https://img.shields.io/badge/Next.js-14-black.svg)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Problem Statement

Customer service teams receive thousands of audio recordings daily but lack efficient tools to:
- Quickly identify high-priority issues and complaints
- Detect sentiment and emotional states in conversations
- Extract actionable insights from multilingual calls
- Prioritize urgent cases requiring immediate attention
- Analyze patterns across large volumes of recordings

**SARCIS solves this** by automatically transcribing, translating, and analyzing audio files to provide rich, actionable intelligence in seconds.

## ✨ Key Features

### 🚀 Ultra-Fast Processing
- **Groq Whisper API**: 3-10 seconds per file transcription
- **Automatic Fallback**: Local Whisper model ensures 100% reliability
- **Total Processing**: 5-15 seconds per audio file

### 🧠 Advanced AI Analysis
- **Speech Recognition**: Whisper large-v3 (Groq) with medium fallback
- **Multilingual Support**: Hindi, English, and Hinglish translation
- **LLM Intelligence**: Llama 3.3 70B for contextual understanding

### 📊 Rich Insights Extraction
- **Sentiment Analysis**: Type (positive/negative/aggressive) + intensity score
- **Intent Detection**: Identify the primary purpose of each call
- **Risk Assessment**: Low, moderate, high, or extreme risk levels
- **Priority Classification**: Critical, high, medium, or low urgency
- **Event Detection**: Complaints, threats, escalations, technical issues
- **Entity Extraction**: Names, products, amounts, dates mentioned

### 💻 Interactive Dashboard
- Real-time cluster and file-level analytics
- Audio playback with segment navigation
- Visual insights and trend analysis
- File ranking by importance score

## 🏗️ Architecture

### System Overview

```
┌─────────────┐
│   Frontend  │  Next.js 14 + TypeScript + Tailwind CSS
│  (React UI) │
└──────┬──────┘
       │ HTTP/REST
       ↓
┌─────────────┐
│   Backend   │  FastAPI + Python
│  (API Layer)│
└──────┬──────┘
       │
       ├─→ MongoDB (Data Storage)
       │
       └─→ Processing Pipeline:
           ┌──────────────────────────────────┐
           │ 1. Audio Upload                  │
           ├──────────────────────────────────┤
           │ 2. Transcription                 │
           │    ├─→ Try: Groq Whisper API     │
           │    └─→ Fallback: Local Whisper   │
           ├──────────────────────────────────┤
           │ 3. Translation (if needed)       │
           │    └─→ Helsinki NLP (Hi→En)      │
           ├──────────────────────────────────┤
           │ 4. LLM Analysis                  │
           │    └─→ Groq Llama 3.3 70B        │
           ├──────────────────────────────────┤
           │ 5. Insights Generation           │
           │    └─→ Segment + Cluster Level   │
           └──────────────────────────────────┘
```

### Tech Stack

**Backend**
- **FastAPI**: Modern Python web framework
- **MongoDB**: Document database for flexible data storage
- **Whisper**: OpenAI's speech recognition (local fallback)
- **Groq**: Fast LLM inference (Whisper + Llama 3.3 70B)
- **Transformers**: Helsinki NLP for Hindi-English translation

**Frontend**
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **Framer Motion**: Smooth animations

## 🔄 How It Works

### 1. Audio Upload
Users upload MP3 audio files organized into clusters (projects/campaigns).

### 2. Transcription (Fast)
- **Primary**: Groq Whisper API transcribes audio in 3-10 seconds
- **Fallback**: Local Whisper model (40-90s) if API fails
- **Output**: Full transcript with timestamps

### 3. Translation (If Needed)
- Detects language (Hindi/English/Hinglish)
- Translates non-English content to English
- Preserves original text for reference

### 4. LLM Analysis (Once per File)
- Sends full transcript to Llama 3.3 70B
- Extracts comprehensive intelligence:
  - Overall sentiment + intensity
  - Primary intent
  - Risk level and urgency
  - Key events and entities
  - Contextual summary

### 5. Insights Generation
- **Segment Level**: Each audio segment inherits file-level intelligence
- **File Level**: Summary statistics and top issues
- **Cluster Level**: Aggregated analytics across all files

### 6. Dashboard Visualization
- Interactive UI displays all insights
- Audio playback with segment jumping
- Filtering and sorting by priority/sentiment
- Export capabilities for reporting

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- MongoDB Atlas account (or local MongoDB)
- Groq API key ([Get free key](https://console.groq.com/))

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/satvik-sharma-05/SARCIS-.git
cd SARCIS-
```

**2. Backend Setup**
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp ../.env.example .env
# Edit .env with your MongoDB URI and Groq API key

# Start backend
python main.py
```

Backend runs on `http://localhost:8000`

**3. Frontend Setup**
```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env.local

# Start development server
npm run dev
```

Frontend runs on `http://localhost:3000`

### Usage

1. **Sign Up**: Create an account at http://localhost:3000/signup
2. **Create Cluster**: Organize your audio files into projects
3. **Upload Files**: Upload MP3 audio recordings
4. **Analyze**: Click "Analyze" to process files (5-15 seconds each)
5. **Explore**: View insights, play audio, and export results

## 📊 Performance Metrics

| Metric | Value | Details |
|--------|-------|---------|
| **Transcription** | 3-10s | Groq Whisper API (primary) |
| **Fallback** | 40-90s | Local Whisper (if API fails) |
| **Translation** | 1-2s | Helsinki NLP model |
| **LLM Analysis** | 1-3s | Groq Llama 3.3 70B |
| **Total** | **5-15s** | Complete processing per file |
| **Accuracy** | High | Whisper large-v3 + 70B LLM |
| **Reliability** | 100% | Automatic fallback system |

## 🔧 Configuration

### Environment Variables

**Backend (.env)**
```env
# MongoDB
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
MONGODB_DB_NAME=sarcis

# JWT Secret
JWT_SECRET_KEY=your-secret-key-change-in-production

# Whisper Model (for fallback)
WHISPER_MODEL=medium

# Groq API
GROQ_API_KEY=your_groq_api_key_here
```

**Frontend (.env.local)**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📁 Project Structure

```
SARCIS/
├── backend/
│   ├── main.py              # FastAPI application & routes
│   ├── db.py                # MongoDB connection
│   ├── models.py            # Data models
│   ├── requirements.txt     # Python dependencies
│   └── services/
│       ├── auth.py          # Authentication logic
│       └── processor.py     # Audio processing pipeline
├── frontend/
│   ├── app/                 # Next.js pages (App Router)
│   │   ├── login/           # Login page
│   │   ├── signup/          # Signup page
│   │   ├── dashboard/       # Main dashboard
│   │   ├── cluster/[id]/    # Cluster details
│   │   └── results/[id]/    # Analysis results
│   ├── lib/
│   │   ├── api.ts           # API client
│   │   └── auth-context.tsx # Auth context
│   └── package.json         # Node dependencies
├── .env.example             # Environment template
├── .gitignore               # Git ignore rules
├── LICENSE                  # MIT License
├── README.md                # This file
└── Tutorial.md              # Detailed technical guide
```

## 🎯 Use Cases

- **Customer Service**: Analyze support call recordings for quality assurance
- **Sales**: Identify objections and sentiment in sales calls
- **Compliance**: Detect policy violations and risk indicators
- **Market Research**: Extract insights from customer interviews
- **Training**: Evaluate agent performance and identify coaching opportunities

## 🔒 Security

- JWT-based authentication
- Password hashing with bcrypt
- Environment variable protection
- MongoDB connection security
- API key management

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) for speech recognition
- [Groq](https://groq.com/) for fast LLM inference
- [Helsinki NLP](https://huggingface.co/Helsinki-NLP) for translation models
- [FastAPI](https://fastapi.tiangolo.com/) and [Next.js](https://nextjs.org/) communities

## 📞 Contact

For questions or support, please open an issue on GitHub.

---

**Built with ❤️ for better customer service insights**
