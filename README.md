# SARCIS - Smart Audio Risk & Context Intelligence System

An AI-powered audio analysis platform that extracts deep insights from customer service call recordings using advanced speech recognition, translation, and LLM-based intelligence.

## 🚀 Features

- **Advanced Speech Recognition**: Whisper medium model for high-accuracy transcription
- **Multilingual Support**: Automatic Hindi/English/Hinglish translation
- **LLM Intelligence**: 70B parameter model (Llama 3.3) for contextual analysis
- **Rich Insights**: Sentiment, intent, risk level, urgency, and entity extraction
- **Real-time Dashboard**: Interactive UI for cluster and file-level analytics
- **Audio Playback**: Synchronized audio player with segment navigation
- **Optimized Performance**: 1-2 minutes per file processing time

## 📊 What It Analyzes

For each audio file, SARCIS provides:

- **Sentiment Analysis**: Type (positive/negative/aggressive/frustrated) + intensity
- **Intent Detection**: Primary purpose of the call
- **Risk Assessment**: Low, moderate, high, or extreme risk levels
- **Priority Classification**: Critical, high, medium, or low priority
- **Event Detection**: Complaints, threats, escalations, technical issues
- **Entity Extraction**: Names, products, amounts, dates mentioned
- **Summary**: Concise explanation of the conversation

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **MongoDB**: Document database for flexible data storage
- **Whisper**: OpenAI's speech recognition model
- **Groq**: Fast LLM inference with Llama 3.3 70B
- **Transformers**: Helsinki NLP for Hindi-English translation

### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **Framer Motion**: Smooth animations

## 📦 Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- MongoDB Atlas account (or local MongoDB)
- Groq API key ([Get one here](https://console.groq.com/))

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp ../.env.example .env

# Edit .env with your credentials
# - Add your MongoDB URI
# - Add your Groq API key
# - Configure Whisper model (default: medium)

# Start the backend
python main.py
```

The backend will start on `http://localhost:8000`

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Copy environment template
cp .env.example .env.local

# Start the development server
npm run dev
```

The frontend will start on `http://localhost:3000`

## 🎯 Quick Start

1. **Sign Up**: Create an account at http://localhost:3000/signup
2. **Create Cluster**: Organize your audio files into clusters
3. **Upload Files**: Upload MP3 audio files (customer service recordings)
4. **Analyze**: Click "Analyze" to process the files
5. **View Results**: Explore insights, segments, and analytics

## 📈 Performance

- **Processing Speed**: 1-2 minutes per audio file
- **Model Loading**: ~30 seconds on first startup
- **Accuracy**: High (Whisper medium + 70B LLM)
- **Scalability**: Sequential processing for stability

## 🔧 Configuration

### Whisper Model Options

In `.env`, you can configure the Whisper model:

```env
WHISPER_MODEL=medium  # Recommended (balanced speed/accuracy)
# WHISPER_MODEL=small  # Faster but less accurate
# WHISPER_MODEL=large  # More accurate but slower
```

### Processing Workers

In `backend/services/processor.py`, you can adjust parallel processing:

```python
# Currently set to sequential (most stable)
# For parallel processing, modify the process_cluster function
```

## 📁 Project Structure

```
SARCIS/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── db.py                # MongoDB connection
│   ├── models.py            # Data models
│   ├── requirements.txt     # Python dependencies
│   └── services/
│       ├── auth.py          # Authentication logic
│       └── processor.py     # Audio processing pipeline
├── frontend/
│   ├── app/                 # Next.js pages
│   ├── lib/                 # API client & utilities
│   └── package.json         # Node dependencies
├── .env.example             # Environment template
└── README.md                # This file
```

## � Troubleshooting

### "sacremoses not found"
```bash
pip install sacremoses==0.1.1
```

### "Groq API key invalid"
Check your `.env` file has a valid API key from https://console.groq.com/

### "Out of memory"
Reduce the Whisper model size in `.env`:
```env
WHISPER_MODEL=small
```

### "Slow transcription"
This is normal for Whisper medium on CPU. Expected: 40-90 seconds per file.

## 📚 Documentation

- [Optimization Guide](OPTIMIZATION_COMPLETE.md) - Performance improvements
- [Threading Fix](THREADING_FIX.md) - PyTorch thread safety
- [Quick Start](QUICK_START.md) - Fast setup guide
- [API Documentation](API_DOCUMENTATION.md) - API endpoints

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI Whisper for speech recognition
- Groq for fast LLM inference
- Helsinki NLP for translation models
- FastAPI and Next.js communities

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review troubleshooting guide

---

**Built with ❤️ for better customer service insights**
