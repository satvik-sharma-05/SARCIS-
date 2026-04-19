"""
Test script for Phase 1 implementation
Run this after starting the backend to verify everything works
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_health():
    """Test health endpoint"""
    print_section("Testing Health Endpoint")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_signup():
    """Test user signup"""
    print_section("Testing User Signup")
    
    # Generate unique email
    email = f"test_{datetime.now().timestamp()}@example.com"
    
    data = {
        "email": email,
        "password": "SecurePass123!",
        "name": "Test User"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/signup", json=data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 201:
        result = response.json()
        print(f"✅ User created: {result['user']['email']}")
        print(f"✅ Access token received: {result['access_token'][:20]}...")
        return result['access_token']
    else:
        print(f"❌ Signup failed: {response.text}")
        return None

def test_login(email, password):
    """Test user login"""
    print_section("Testing User Login")
    
    data = {
        "email": email,
        "password": password
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/login", json=data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Login successful")
        return result['access_token']
    else:
        print(f"❌ Login failed: {response.text}")
        return None

def test_get_current_user(token):
    """Test get current user"""
    print_section("Testing Get Current User")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        user = response.json()
        print(f"✅ User info retrieved:")
        print(f"   Email: {user['email']}")
        print(f"   Name: {user['name']}")
        print(f"   ID: {user['id']}")
        return True
    else:
        print(f"❌ Failed: {response.text}")
        return False

def test_create_cluster(token):
    """Test cluster creation"""
    print_section("Testing Cluster Creation")
    
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "name": f"Test Cluster {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "description": "Automated test cluster"
    }
    
    response = requests.post(f"{BASE_URL}/api/clusters", json=data, headers=headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 201:
        cluster = response.json()
        print(f"✅ Cluster created:")
        print(f"   ID: {cluster['id']}")
        print(f"   Name: {cluster['name']}")
        print(f"   Status: {cluster['status']}")
        return cluster['id']
    else:
        print(f"❌ Failed: {response.text}")
        return None

def test_list_clusters(token):
    """Test listing clusters"""
    print_section("Testing List Clusters")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/clusters", headers=headers)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Found {len(result['clusters'])} cluster(s)")
        for cluster in result['clusters']:
            print(f"   - {cluster['name']} (ID: {cluster['id']})")
        return True
    else:
        print(f"❌ Failed: {response.text}")
        return False

def test_get_cluster(token, cluster_id):
    """Test getting cluster details"""
    print_section("Testing Get Cluster Details")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/clusters/{cluster_id}", headers=headers)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        cluster = response.json()
        print(f"✅ Cluster details:")
        print(f"   Name: {cluster['name']}")
        print(f"   File Count: {cluster['file_count']}")
        print(f"   Status: {cluster['status']}")
        return True
    else:
        print(f"❌ Failed: {response.text}")
        return False

def test_update_cluster(token, cluster_id):
    """Test updating cluster"""
    print_section("Testing Update Cluster")
    
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "name": "Updated Test Cluster",
        "description": "Updated description"
    }
    
    response = requests.put(f"{BASE_URL}/api/clusters/{cluster_id}", json=data, headers=headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        cluster = response.json()
        print(f"✅ Cluster updated:")
        print(f"   New Name: {cluster['name']}")
        return True
    else:
        print(f"❌ Failed: {response.text}")
        return False

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("  PHASE 1 INTEGRATION TESTS")
    print("="*60)
    
    results = []
    
    # Test 1: Health check
    results.append(("Health Check", test_health()))
    
    # Test 2: Signup
    token = test_signup()
    results.append(("User Signup", token is not None))
    
    if not token:
        print("\n❌ Cannot continue without authentication token")
        return
    
    # Test 3: Get current user
    results.append(("Get Current User", test_get_current_user(token)))
    
    # Test 4: Create cluster
    cluster_id = test_create_cluster(token)
    results.append(("Create Cluster", cluster_id is not None))
    
    if not cluster_id:
        print("\n❌ Cannot continue without cluster")
        return
    
    # Test 5: List clusters
    results.append(("List Clusters", test_list_clusters(token)))
    
    # Test 6: Get cluster details
    results.append(("Get Cluster Details", test_get_cluster(token, cluster_id)))
    
    # Test 7: Update cluster
    results.append(("Update Cluster", test_update_cluster(token, cluster_id)))
    
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
        print("🎉 All tests passed! Phase 1 is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    try:
        run_all_tests()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to backend server")
        print("Make sure the backend is running on http://localhost:8000")
        print("\nStart the backend with:")
        print("  cd backend")
        print("  python main.py")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
