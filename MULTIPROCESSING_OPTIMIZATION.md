# Multiprocessing Optimization Guide

## Problem Statement

### Before Optimization ❌
```python
# OLD APPROACH - INEFFICIENT
whisper_model = whisper.load_model("base")  # Loaded at module level
sentiment_analyzer = pipeline(...)           # Loaded at module level

def process_file(file):
    # Each worker process loads models again!
    # This happens N times for N processes
    result = whisper_model.transcribe(file)  # Uses model
```

**Issues:**
- Models loaded multiple times (once per worker process startup)
- High memory usage (duplicate models in memory)
- Slow startup (each worker loads models independently)
- Wasted computation

### After Optimization ✅
```python
# NEW APPROACH - EFFICIENT
whisper_model = None  # Global variable
sentiment_analyzer = None

def init_worker():
    """Load models ONCE per worker process"""
    global whisper_model, sentiment_analyzer
    whisper_model = whisper.load_model("base")
    sentiment_analyzer = pipeline(...)

def process_file(file):
    """Reuse pre-loaded models"""
    global whisper_model, sentiment_analyzer
    result = whisper_model.transcribe(file)

# Use Pool with initializer
with Pool(processes=4, initializer=init_worker) as pool:
    results = pool.map(process_file, files)
```

**Benefits:**
- Models loaded once per worker (not per file)
- Lower memory usage
- Faster processing
- Efficient resource utilization

## How It Works

### 1. Global Model Variables
```python
# These are None initially
whisper_model = None
sentiment_analyzer = None
translator_model = None
translator_tokenizer = None
```

### 2. Worker Initialization Function
```python
def init_worker():
    """
    Called ONCE when each worker process starts.
    Loads all models into global variables.
    """
    global whisper_model, sentiment_analyzer, translator_model, translator_tokenizer
    
    print(f"🔧 Initializing worker process...")
    
    # Load Whisper (once per worker)
    whisper_model = whisper.load_model("base")
    
    # Load sentiment analyzer (once per worker)
    sentiment_analyzer = pipeline("sentiment-analysis", ...)
    
    # Load translator (once per worker)
    translator_tokenizer = MarianTokenizer.from_pretrained(...)
    translator_model = MarianMTModel.from_pretrained(...)
    
    print("✅ Worker initialized with all models")
```

### 3. Processing Function
```python
def process_single_file(args):
    """
    Uses pre-loaded models from global variables.
    Does NOT load models here!
    """
    global whisper_model, sentiment_analyzer
    
    file_record, cluster_id = args
    
    # Use pre-loaded models
    result = whisper_model.transcribe(file_path)
    sentiment = sentiment_analyzer(text)
    
    return processed_result
```

### 4. Pool with Initializer
```python
# Determine optimal number of processes
num_processes = min(4, max(1, cpu_count() // 2))

# Create pool with initializer
# init_worker() is called once per worker process
with Pool(processes=num_processes, initializer=init_worker) as pool:
    results = pool.map(process_single_file, args_list)
```

## Process Flow

```
Main Process
    │
    ├─ Create Pool(processes=4, initializer=init_worker)
    │
    ├─ Worker 1 starts
    │   └─ init_worker() called
    │       └─ Load Whisper, NLP, Translator
    │       └─ Store in global variables
    │   └─ Ready to process files
    │
    ├─ Worker 2 starts
    │   └─ init_worker() called
    │       └─ Load Whisper, NLP, Translator
    │       └─ Store in global variables
    │   └─ Ready to process files
    │
    ├─ Worker 3 starts
    │   └─ init_worker() called
    │       └─ Load Whisper, NLP, Translator
    │       └─ Store in global variables
    │   └─ Ready to process files
    │
    ├─ Worker 4 starts
    │   └─ init_worker() called
    │       └─ Load Whisper, NLP, Translator
    │       └─ Store in global variables
    │   └─ Ready to process files
    │
    └─ Distribute files to workers
        │
        ├─ Worker 1: process file_1.mp3 (reuse models)
        ├─ Worker 2: process file_2.mp3 (reuse models)
        ├─ Worker 3: process file_3.mp3 (reuse models)
        ├─ Worker 4: process file_4.mp3 (reuse models)
        │
        ├─ Worker 1: process file_5.mp3 (reuse models)
        ├─ Worker 2: process file_6.mp3 (reuse models)
        └─ ... (models are reused for all files)
```

## Key Optimizations

### 1. Process Count
```python
# Use half of available CPUs (max 4)
num_processes = min(4, max(1, cpu_count() // 2))
```

**Why?**
- Whisper is CPU-intensive
- Using all CPUs can cause system overload
- Half of CPUs provides good balance
- Max 4 processes to limit memory usage

### 2. Model Selection
```python
whisper_model = whisper.load_model("base")
```

**Options:**
- `tiny` - Fastest, least accurate
- `base` - Good balance (recommended)
- `small` - Better accuracy, slower
- `medium` - High accuracy, much slower
- `large` - Best accuracy, very slow

### 3. Memory Management
- Each worker loads models once
- Models stay in memory for worker lifetime
- Workers reuse models for all files
- Pool is closed after processing (frees memory)

## Performance Comparison

### Before Optimization
```
Processing 10 files with 4 workers:
- Worker 1: Load models (30s) + Process 3 files (90s) = 120s
- Worker 2: Load models (30s) + Process 3 files (90s) = 120s
- Worker 3: Load models (30s) + Process 2 files (60s) = 90s
- Worker 4: Load models (30s) + Process 2 files (60s) = 90s
Total: ~120s (models loaded 4 times)
```

### After Optimization
```
Processing 10 files with 4 workers:
- Worker 1: Load models (30s) + Process 3 files (90s) = 120s
- Worker 2: Load models (30s) + Process 3 files (90s) = 120s
- Worker 3: Load models (30s) + Process 2 files (60s) = 90s
- Worker 4: Load models (30s) + Process 2 files (60s) = 90s
Total: ~120s (models loaded 4 times ONCE, then reused)

But for subsequent batches:
- Worker 1: Process 3 files (90s) = 90s (no loading!)
- Worker 2: Process 3 files (90s) = 90s (no loading!)
- Worker 3: Process 2 files (60s) = 60s (no loading!)
- Worker 4: Process 2 files (60s) = 60s (no loading!)
Total: ~90s (25% faster!)
```

## Code Structure

### processor.py Structure
```python
# 1. Imports
import whisper, transformers, etc.

# 2. Global model variables
whisper_model = None
sentiment_analyzer = None
translator_model = None

# 3. Worker initialization
def init_worker():
    """Load models once per worker"""
    global whisper_model, sentiment_analyzer, translator_model
    # Load all models

# 4. Helper functions
def translate_to_english(text, lang):
    """Use pre-loaded translator"""
    global translator_model
    # Use model

def classify_events(text):
    """Rule-based classification"""
    # No models needed

# 5. Main processing function
def process_single_file(args):
    """Process file using pre-loaded models"""
    global whisper_model, sentiment_analyzer
    # Use models

# 6. Cluster processing
async def process_cluster(cluster_id, files):
    """Orchestrate multiprocessing"""
    with Pool(processes=N, initializer=init_worker) as pool:
        results = pool.map(process_single_file, files)
```

## Best Practices

### ✅ DO
- Use `Pool(initializer=init_worker)` for model loading
- Store models in global variables
- Reuse models across all files in a worker
- Limit number of processes (half of CPUs, max 4)
- Close pool after processing

### ❌ DON'T
- Load models inside `process_single_file()`
- Create new model instances for each file
- Use all available CPUs (causes overload)
- Keep pool open indefinitely
- Use threads for CPU-intensive work

## Troubleshooting

### Issue: Models not found in worker
```python
# Problem: Models are None in worker
def process_single_file(args):
    global whisper_model  # Missing!
    result = whisper_model.transcribe(...)  # Error: None

# Solution: Declare global
def process_single_file(args):
    global whisper_model, sentiment_analyzer  # ✅
    result = whisper_model.transcribe(...)
```

### Issue: High memory usage
```python
# Problem: Too many processes
num_processes = cpu_count()  # 16 processes = 16x models!

# Solution: Limit processes
num_processes = min(4, max(1, cpu_count() // 2))  # Max 4
```

### Issue: Slow startup
```python
# Problem: Large model
whisper_model = whisper.load_model("large")  # Very slow

# Solution: Use smaller model
whisper_model = whisper.load_model("base")  # Faster
```

## Summary

The optimized multiprocessing approach:
1. Loads models once per worker process (not per file)
2. Reuses models across all files processed by that worker
3. Limits number of processes to avoid overload
4. Provides significant performance improvement
5. Keeps code simple and readable

**Result:** Faster processing, lower memory usage, better resource utilization!
