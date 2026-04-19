"""
Test script for Phase 2 implementation
Tests job queue, workers, and audio processing
"""
import requests
import json
import time
from datetime import datetime
from pathlib import Path

BASE_URL = "http://localhost:8000"

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def create_test_user():
    """Create test user and return token"""
    print_section("Creating Test User")
    
    email = f"test_{datetime.now().timestamp()}@example.com"
    data = {
        "email": email,
        "password": "Test123!",
        "name": "Phase 2 Test User"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/signup", json=data)
    
    if response.status_code == 201:
        result = response.json()
        print(f"✅ User created: {result['user']['email']}")
        return result['access_token']
    else:
        print(f"❌ Failed: {response.text}")
        return None

def create_test_cluster(token):
    """Create test cluster"""
    print_section("Creating Test Cluster")
    
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "name": f"Phase 2 Test Cluster {datetime.now().strftime('%H:%M:%S')}",
        "description": "Testing job queue and workers"
    }
    
    response = requests.post(f"{BASE_URL}/api/clusters", json=data, headers=headers)
    
    if response.status_code == 201:
        cluster = response.json()
        print(f"✅ Cluster created: {cluster['name']}")
        print(f"   ID: {cluster['id']}")
        return cluster['id']
    else:
        print(f"❌ Failed: {response.text}")
        return None

def upload_test_file(token, cluster_id):
    """Upload a test audio file"""
    print_section("Uploading Test File")
    
    # Check if test audio directory exists
    test_audio_dir = Path("test_audio")
    if not test_audio_dir.exists():
        print("⚠️  No test_audio directory found")
        print("   Create test_audio/ and add .wav files")
        return None
    
    # Find first audio file
    audio_files = list(test_audio_dir.glob("*.wav")) + \
                  list(test_audio_dir.glob("*.mp3")) + \
                  list(test_audio_dir.glob("*.m4a"))
    
    if not audio_files:
        print("⚠️  No audio files found in test_audio/")
        print("   Add .wav, .mp3, or .m4a files to test_audio/")
        return None
    
    test_file = audio_files[0]
    print(f"📁 Using file: {test_file.name}")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    with open(test_file, 'rb') as f:
        files = {'files': (test_file.name, f, 'audio/wav')}
        response = requests.post(
            f"{BASE_URL}/api/clusters/{cluster_id}/upload",
            headers=headers,
            files=files
        )
    
    if response.status_code == 201:
        result = response.json()
        if result['uploaded_files']:
            file_id = result['uploaded_files'][0]['id']
            print(f"✅ File uploaded: {test_file.name}")
            print(f"   File ID: {file_id}")
            return file_id
        else:
            print(f"❌ Upload failed: {result.get('failed', [])}")
            return None
    else:
        print(f"❌ Failed: {response.text}")
        return None

def start_analysis_job(token, cluster_id):
    """Start analysis job"""
    print_section("Starting Analysis Job")
    
    headers = {"Authorization": f"Bearer {token}"}
    data = {}  # Process all files
    
    response = requests.post(
        f"{BASE_URL}/api/clusters/{cluster_id}/analyze",
        json=data,
        headers=headers
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Job started:")
        print(f"   Job ID: {result['job_id']}")
        print(f"   Status: {result['status']}")
        print(f"   Total files: {result['total_files']}")
        return result['job_id']
    else:
        print(f"❌ Failed: {response.text}")
        return None

def monitor_job_progress(token, job_id, max_wait=300):
    """Monitor job progress until completion"""
    print_section("Monitoring Job Progress")
    
    headers = {"Authorization": f"Bearer {token}"}
    start_time = time.time()
    last_progress = -1
    
    print("⏳ Waiting for job to complete...")
    print("   (This may take a few minutes depending on file size)")
    print()
    
    while True:
        response = requests.get(f"{BASE_URL}/api/jobs/{job_id}", headers=headers)
        
        if response.status_code != 200:
            print(f"❌ Failed to get job status: {response.text}")
            return False
        
        job = response.json()
        status = job['status']
        progress = job['progress']
        processed = job['processed_files']
        total = job['total_files']
        
        # Print progress if changed
        if progress != last_progress:
            print(f"   Status: {status} | Progress: {progress:.1f}% ({processed}/{total} files)")
            last_progress = progress
        
        # Check if completed
        if status == "completed":
            print(f"\n✅ Job completed successfully!")
            print(f"   Total time: {time.time() - start_time:.1f} seconds")
            return True
        
        # Check if failed
        if status == "failed":
            print(f"\n❌ Job failed: {job.get('error_message', 'Unknown error')}")
            return False
        
        # Check timeout
        if time.time() - start_time > max_wait:
            print(f"\n⏱️  Timeout after {max_wait} seconds")
            print(f"   Job is still {status} at {progress:.1f}%")
            return False
        
        # Wait before next check
        time.sleep(2)

def view_results(token, cluster_id):
    """View analysis results"""
    print_section("Viewing Results")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get analytics
    response = requests.get(
        f"{BASE_URL}/api/clusters/{cluster_id}/analytics",
        headers=headers
    )
    
    if response.status_code == 200:
        analytics = response.json()
        print("📊 Cluster Analytics:")
        print(f"   Total files: {analytics['total_files']}")
        print(f"   Total segments: {analytics['total_segments']}")
        print(f"   Total duration: {analytics['total_duration']:.1f}s")
        print()
        
        if analytics['events']:
            print("   Events detected:")
            for event, count in analytics['events'].items():
                print(f"      {event}: {count}")
        
        if analytics['sentiment']:
            print()
            print("   Sentiment distribution:")
            for sentiment, count in analytics['sentiment'].items():
                print(f"      {sentiment}: {count}")
        
        if analytics['priority']:
            print()
            print("   Priority distribution:")
            for priority, count in analytics['priority'].items():
                print(f"      {priority}: {count}")
    else:
        print(f"❌ Failed to get analytics: {response.text}")
        return False
    
    # Get segments
    print()
    response = requests.get(
        f"{BASE_URL}/api/clusters/{cluster_id}/segments?limit=5",
        headers=headers
    )
    
    if response.status_code == 200:
        result = response.json()
        segments = result['segments']
        total = result['pagination']['total']
        
        print(f"📝 Sample Segments (showing 5 of {total}):")
        print()
        
        for i, segment in enumerate(segments[:5], 1):
            print(f"   Segment {i}:")
            print(f"      Time: {segment['start']:.1f}s - {segment['end']:.1f}s")
            print(f"      Text: {segment['text'][:80]}...")
            print(f"      Events: {', '.join(segment['events'])}")
            print(f"      Sentiment: {segment['sentiment']}")
            print(f"      Priority: {segment['priority']}")
            print()
        
        return True
    else:
        print(f"❌ Failed to get segments: {response.text}")
        return False

def check_prerequisites():
    """Check if Redis and workers are running"""
    print_section("Checking Prerequisites")
    
    # Check backend
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            health = response.json()
            print(f"✅ Backend: Running")
            print(f"   Database: {health.get('database', 'unknown')}")
        else:
            print(f"❌ Backend: Not responding")
            return False
    except:
        print(f"❌ Backend: Cannot connect to {BASE_URL}")
        print("   Make sure backend is running: python backend/main.py")
        return False
    
    # Check Redis (indirectly by checking if we can create a job)
    print(f"✅ Redis: Will be tested during job creation")
    
    # Check workers
    print(f"⚠️  Workers: Cannot check directly")
    print("   Make sure workers are running:")
    print("   - Windows: backend/start_worker.bat")
    print("   - Linux/Mac: backend/start_worker.sh")
    
    return True

def run_full_test():
    """Run complete Phase 2 test"""
    print("\n" + "="*60)
    print("  PHASE 2 INTEGRATION TEST")
    print("  Job Queue + Workers + Audio Processing")
    print("="*60)
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n❌ Prerequisites not met. Please fix and try again.")
        return
    
    print("\n⚠️  Make sure you have:")
    print("   1. Redis running (docker run -d -p 6379:6379 redis)")
    print("   2. Backend running (python backend/main.py)")
    print("   3. Worker running (./backend/start_worker.sh)")
    print("   4. Audio file in test_audio/ directory")
    
    input("\nPress Enter to continue...")
    
    # Run tests
    results = []
    
    # 1. Create user
    token = create_test_user()
    results.append(("Create User", token is not None))
    if not token:
        return
    
    # 2. Create cluster
    cluster_id = create_test_cluster(token)
    results.append(("Create Cluster", cluster_id is not None))
    if not cluster_id:
        return
    
    # 3. Upload file
    file_id = upload_test_file(token, cluster_id)
    results.append(("Upload File", file_id is not None))
    if not file_id:
        return
    
    # 4. Start job
    job_id = start_analysis_job(token, cluster_id)
    results.append(("Start Job", job_id is not None))
    if not job_id:
        return
    
    # 5. Monitor progress
    completed = monitor_job_progress(token, job_id)
    results.append(("Job Completion", completed))
    if not completed:
        return
    
    # 6. View results
    results_ok = view_results(token, cluster_id)
    results.append(("View Results", results_ok))
    
    # Print summary
    print_section("TEST SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n{'='*60}")
    print(f"  Results: {passed}/{total} tests passed")
    print(f"{'='*60}\n")
    
    if passed == total:
        print("🎉 Phase 2 is working perfectly!")
        print("\nYour system can now:")
        print("  ✅ Queue background jobs")
        print("  ✅ Process audio files with workers")
        print("  ✅ Track progress in real-time")
        print("  ✅ Store results in database")
        print("  ✅ Compute analytics")
        print("  ✅ Retrieve and display results")
    else:
        print("⚠️  Some tests failed. Check the output above.")

if __name__ == "__main__":
    try:
        run_full_test()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to backend")
        print("Make sure backend is running: python backend/main.py")
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
