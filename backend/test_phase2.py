"""
DevMind Phase 2 Test Suite
Comprehensive testing of advanced code analysis features
"""

import asyncio
import json
import requests
import time
from typing import Dict, List, Any

# Test configuration
BASE_URL = "http://localhost:8001"
TEST_USER_ID = "test_user_123"

# Sample code for testing
SAMPLE_PYTHON_CODE = '''
def calculate_fibonacci(n):
    if n <= 1:
        return n
    else:
        return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

class Calculator:
    def __init__(self):
        self.result = 0
    
    def add(self, a, b):
        result = a + b
        return result
    
    def divide(self, a, b):
        return a / b  # Potential division by zero
    
    def complex_function(self, x, y, z, w, v, u):  # Too many parameters
        if x > 0:
            if y > 0:
                if z > 0:
                    if w > 0:
                        if v > 0:
                            return u  # Deep nesting
        return 0

# Hardcoded password - security issue
PASSWORD = "admin123"
API_KEY = "sk-1234567890abcdef"

def unsafe_eval(user_input):
    return eval(user_input)  # Dangerous function
'''

SAMPLE_JAVASCRIPT_CODE = '''
function calculateSum(a, b) {
    return a + b;
}

class UserManager {
    constructor() {
        this.users = [];
    }
    
    addUser(user) {
        this.users.push(user);
    }
    
    getUserById(id) {
        for (let i = 0; i < this.users.length; i++) {
            if (this.users[i].id === id) {
                return this.users[i];
            }
        }
        return null;
    }
}

// Duplicate code
function processData(data) {
    if (data.length > 0) {
        console.log("Processing data");
        return data.map(item => item.value);
    }
    return [];
}

function handleData(items) {
    if (items.length > 0) {
        console.log("Processing data");
        return items.map(item => item.value);
    }
    return [];
}
'''

SAMPLE_COMMITS = [
    {
        "message": "feat(auth): add user authentication system",
        "timestamp": "2025-01-15T10:30:00Z",
        "files_changed": ["auth.py", "models.py", "tests/test_auth.py"],
        "lines_added": 120,
        "lines_removed": 15
    },
    {
        "message": "fix: resolve login validation bug",
        "timestamp": "2025-01-15T14:20:00Z", 
        "files_changed": ["auth.py"],
        "lines_added": 8,
        "lines_removed": 3
    },
    {
        "message": "docs: update API documentation",
        "timestamp": "2025-01-16T09:15:00Z",
        "files_changed": ["README.md", "docs/api.md"],
        "lines_added": 45,
        "lines_removed": 12
    }
]

def print_test_header(test_name: str):
    """Print formatted test header"""
    print(f"\n{'='*60}")
    print(f"🧪 {test_name}")
    print(f"{'='*60}")

def print_test_result(test_name: str, success: bool, details: str = ""):
    """Print test result"""
    status = "✅ PASSED" if success else "❌ FAILED"
    print(f"{status} - {test_name}")
    if details:
        print(f"   Details: {details}")
    print()

def test_health_check():
    """Test health check endpoint"""
    print_test_header("Health Check")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        
        if response.status_code == 200:
            data = response.json()
            
            # Check required fields
            required_fields = ["status", "version", "ai_engine", "agents"]
            missing_fields = [field for field in required_fields if field not in data]
            
            if not missing_fields and data["status"] == "healthy":
                print_test_result("Health Check", True, f"Version: {data.get('version', 'N/A')}")
                print(f"   Active agents: {len(data.get('agents', {}))}")
                return True
            else:
                print_test_result("Health Check", False, f"Missing fields: {missing_fields}")
                return False
        else:
            print_test_result("Health Check", False, f"HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print_test_result("Health Check", False, str(e))
        return False

def test_advanced_code_analysis():
    """Test advanced code analysis endpoint"""
    print_test_header("Advanced Code Analysis")
    
    try:
        payload = {
            "code": SAMPLE_PYTHON_CODE,
            "language": "python",
            "file_path": "/test/sample.py",
            "analysis_type": "comprehensive",
            "user_id": TEST_USER_ID,
            "include_smells": True,
            "include_complexity": True,
            "include_dependencies": True
        }
        
        response = requests.post(f"{BASE_URL}/api/v2/analyze-code-advanced", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            
            # Check for expected fields
            expected_fields = ["success", "language", "ast_analysis", "code_smells", "smell_summary"]
            present_fields = [field for field in expected_fields if field in data]
            
            smells_count = len(data.get("code_smells", []))
            quality_score = data.get("smell_summary", {}).get("quality_score", 0)
            
            print_test_result(
                "Advanced Code Analysis", 
                data.get("success", False),
                f"Found {smells_count} code smells, Quality score: {quality_score}/100"
            )
            
            # Print some detected smells
            if smells_count > 0:
                print("   🔍 Detected Code Smells:")
                for smell in data["code_smells"][:3]:  # Show first 3
                    print(f"      • {smell['severity'].upper()}: {smell['description']} (Line {smell['line']})")
            
            return data.get("success", False)
        else:
            print_test_result("Advanced Code Analysis", False, f"HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print_test_result("Advanced Code Analysis", False, str(e))
        return False

def test_code_smell_detection():
    """Test dedicated code smell detection"""
    print_test_header("Code Smell Detection")
    
    try:
        payload = {
            "code": SAMPLE_PYTHON_CODE,
            "file_path": "/test/smelly_code.py",
            "language": "python",
            "user_id": TEST_USER_ID
        }
        
        response = requests.post(f"{BASE_URL}/api/v2/detect-code-smells", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            
            smells = data.get("smells", [])
            summary = data.get("summary", {})
            
            # Categorize smells by severity
            severity_counts = {}
            for smell in smells:
                severity = smell.get("severity", "unknown")
                severity_counts[severity] = severity_counts.get(severity, 0) + 1
            
            print_test_result(
                "Code Smell Detection",
                data.get("success", False),
                f"Total: {len(smells)}, Critical: {severity_counts.get('critical', 0)}, High: {severity_counts.get('high', 0)}"
            )
            
            # Show different categories
            categories = {}
            for smell in smells:
                cat = smell.get("category", "unknown")
                categories[cat] = categories.get(cat, 0) + 1
            
            if categories:
                print("   📊 Smell Categories:")
                for category, count in categories.items():
                    print(f"      • {category}: {count}")
            
            return data.get("success", False)
        else:
            print_test_result("Code Smell Detection", False, f"HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print_test_result("Code Smell Detection", False, str(e))
        return False

def test_learning_system():
    """Test learning and personalization system"""
    print_test_header("Learning System")
    
    try:
        # Test 1: Learn from code style
        style_payload = {
            "user_id": TEST_USER_ID,
            "learning_type": "code_style",
            "data": {
                "code": SAMPLE_PYTHON_CODE,
                "file_path": "/test/style_sample.py",
                "language": "python"
            }
        }
        
        response1 = requests.post(f"{BASE_URL}/api/v2/learn-user-pattern", json=style_payload)
        style_success = response1.status_code == 200 and response1.json().get("success", False)
        
        # Test 2: Learn from commit patterns
        commit_payload = {
            "user_id": TEST_USER_ID,
            "learning_type": "commit_pattern",
            "data": {
                "commits": SAMPLE_COMMITS
            }
        }
        
        response2 = requests.post(f"{BASE_URL}/api/v2/learn-user-pattern", json=commit_payload)
        commit_success = response2.status_code == 200 and response2.json().get("success", False)
        
        # Test 3: Get personalized recommendations
        rec_payload = {
            "user_id": TEST_USER_ID,
            "context": {
                "language": "python",
                "code": "def badFunctionName():\n  pass",
                "file_path": "/test/style_check.py"
            }
        }
        
        response3 = requests.post(f"{BASE_URL}/api/v2/get-personalized-recommendations", json=rec_payload)
        rec_success = response3.status_code == 200
        
        if rec_success:
            recommendations = response3.json().get("recommendations", {})
            style_suggestions = len(recommendations.get("style_suggestions", []))
            
            print_test_result(
                "Learning System",
                style_success and commit_success and rec_success,
                f"Style learned: {style_success}, Commits: {commit_success}, Suggestions: {style_suggestions}"
            )
            
            if style_suggestions > 0:
                print("   💡 Style Suggestions:")
                for suggestion in recommendations["style_suggestions"][:2]:
                    print(f"      • {suggestion}")
        else:
            print_test_result("Learning System", False, "Failed to get recommendations")
        
        return style_success and commit_success and rec_success
        
    except Exception as e:
        print_test_result("Learning System", False, str(e))
        return False

def test_user_progress():
    """Test user learning progress endpoint"""
    print_test_header("User Learning Progress")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v2/user-learning-progress/{TEST_USER_ID}")
        
        if response.status_code == 200:
            data = response.json()
            progress = data.get("progress", {})
            analytics = data.get("analytics", {})
            
            total_sessions = progress.get("total_sessions", 0)
            learning_streak = progress.get("learning_streak", 0)
            
            print_test_result(
                "User Learning Progress",
                data.get("success", False),
                f"Sessions: {total_sessions}, Streak: {learning_streak} days"
            )
            
            return data.get("success", False)
        else:
            print_test_result("User Learning Progress", False, f"HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print_test_result("User Learning Progress", False, str(e))
        return False

def test_supported_languages():
    """Test supported languages endpoint"""
    print_test_header("Supported Languages")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v2/supported-languages")
        
        if response.status_code == 200:
            data = response.json()
            languages = data.get("languages", [])
            
            language_names = [lang.get("name") for lang in languages]
            
            print_test_result(
                "Supported Languages",
                data.get("success", False) and len(languages) > 0,
                f"Languages: {', '.join(language_names)}"
            )
            
            return data.get("success", False) and len(languages) > 0
        else:
            print_test_result("Supported Languages", False, f"HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print_test_result("Supported Languages", False, str(e))
        return False

def test_javascript_analysis():
    """Test JavaScript code analysis"""
    print_test_header("JavaScript Analysis")
    
    try:
        payload = {
            "code": SAMPLE_JAVASCRIPT_CODE,
            "language": "javascript",
            "file_path": "/test/sample.js",
            "analysis_type": "comprehensive",
            "user_id": TEST_USER_ID
        }
        
        response = requests.post(f"{BASE_URL}/api/v2/analyze-code-advanced", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            
            smells = data.get("code_smells", [])
            js_smells = len(smells)
            
            print_test_result(
                "JavaScript Analysis",
                data.get("success", False),
                f"Analyzed JS code, found {js_smells} issues"
            )
            
            return data.get("success", False)
        else:
            print_test_result("JavaScript Analysis", False, f"HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print_test_result("JavaScript Analysis", False, str(e))
        return False

def test_performance_benchmark():
    """Test performance requirements"""
    print_test_header("Performance Benchmark")
    
    try:
        # Test analysis speed (should be ≤ 2 seconds for 500-1000 lines)
        large_code = SAMPLE_PYTHON_CODE * 20  # Create larger code sample
        
        payload = {
            "code": large_code,
            "language": "python",
            "file_path": "/test/large_file.py",
            "user_id": TEST_USER_ID
        }
        
        start_time = time.time()
        response = requests.post(f"{BASE_URL}/api/v2/analyze-code-advanced", json=payload)
        end_time = time.time()
        
        analysis_time = end_time - start_time
        
        if response.status_code == 200:
            meets_requirement = analysis_time <= 2.0
            
            print_test_result(
                "Performance Benchmark",
                meets_requirement,
                f"Analysis time: {analysis_time:.2f}s (requirement: ≤2s)"
            )
            
            return meets_requirement
        else:
            print_test_result("Performance Benchmark", False, f"HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print_test_result("Performance Benchmark", False, str(e))
        return False

def run_all_tests():
    """Run all Phase 2 tests"""
    print("🚀 DevMind Phase 2 Test Suite")
    print("Testing advanced code analysis features...")
    
    test_results = []
    
    # Run all tests
    tests = [
        ("Health Check", test_health_check),
        ("Advanced Code Analysis", test_advanced_code_analysis),
        ("Code Smell Detection", test_code_smell_detection), 
        ("Learning System", test_learning_system),
        ("User Progress", test_user_progress),
        ("Supported Languages", test_supported_languages),
        ("JavaScript Analysis", test_javascript_analysis),
        ("Performance Benchmark", test_performance_benchmark)
    ]
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            test_results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            test_results.append((test_name, False))
    
    # Print summary
    print_test_header("Test Summary")
    
    passed = sum(1 for _, result in test_results if result)
    total = len(test_results)
    
    print(f"📊 Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print()
    
    for test_name, result in test_results:
        status = "✅" if result else "❌"
        print(f"{status} {test_name}")
    
    if passed == total:
        print(f"\n🎉 All tests passed! Phase 2 implementation is working correctly.")
    else:
        print(f"\n⚠️  {total - passed} tests failed. Check the implementation.")
    
    return passed == total

if __name__ == "__main__":
    # Wait for server to be ready
    print("⏳ Waiting for server to be ready...")
    time.sleep(3)
    
    # Run tests
    success = run_all_tests()
    
    if success:
        print("\n✅ Phase 2 testing completed successfully!")
    else:
        print("\n❌ Some tests failed. Please check the implementation.")