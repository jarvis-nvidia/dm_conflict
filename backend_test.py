#!/usr/bin/env python3
"""
DevMind AI Backend Comprehensive Testing Suite
Tests all backend API endpoints with realistic code samples containing various code smells
"""

import requests
import json
import time
import uuid
from typing import Dict, Any, List

# Backend URL - using the external URL from frontend .env
BACKEND_URL = "https://9e1b2eda-fb7f-47df-b042-a0aaf5a14807.preview.emergentagent.com"

# Test data with various code smells
PYTHON_CODE_WITH_SMELLS = '''
import os
import sys
import time
import requests
from datetime import datetime

# Global variables (code smell: global state)
user_data = {}
config = {"api_key": "hardcoded_key_123", "timeout": 30}

class DataProcessor:
    def __init__(self):
        self.data = []
        self.processed = False
        
    # Long method with high complexity (code smell)
    def process_user_data(self, user_input, validation_type, output_format, debug_mode=False, cache_enabled=True):
        if validation_type == "email":
            if "@" not in user_input:
                if debug_mode:
                    print("Invalid email format")
                return False
            else:
                if "." not in user_input.split("@")[1]:
                    if debug_mode:
                        print("Invalid domain format")
                    return False
                else:
                    if len(user_input) < 5:
                        if debug_mode:
                            print("Email too short")
                        return False
                    else:
                        if cache_enabled:
                            user_data[user_input] = {"validated": True, "timestamp": time.time()}
                        if output_format == "json":
                            return {"valid": True, "email": user_input}
                        else:
                            return True
        elif validation_type == "phone":
            if len(user_input) < 10:
                return False
            else:
                if not user_input.replace("-", "").replace("(", "").replace(")", "").replace(" ", "").isdigit():
                    return False
                else:
                    if cache_enabled:
                        user_data[user_input] = {"validated": True, "timestamp": time.time()}
                    if output_format == "json":
                        return {"valid": True, "phone": user_input}
                    else:
                        return True
        else:
            return False
    
    # Duplicate code (code smell)
    def validate_email_format(self, email):
        if "@" not in email:
            return False
        if "." not in email.split("@")[1]:
            return False
        if len(email) < 5:
            return False
        return True
    
    # Another duplicate with slight variation
    def check_email_validity(self, email_address):
        if "@" not in email_address:
            return False
        if "." not in email_address.split("@")[1]:
            return False
        if len(email_address) < 5:
            return False
        return True
    
    # Magic numbers and hardcoded values (code smell)
    def calculate_score(self, metrics):
        base_score = 100
        if metrics["accuracy"] > 0.85:
            bonus = 25
        elif metrics["accuracy"] > 0.70:
            bonus = 15
        else:
            bonus = 0
        
        penalty = 0
        if metrics["response_time"] > 2000:
            penalty = 20
        elif metrics["response_time"] > 1000:
            penalty = 10
            
        final_score = base_score + bonus - penalty
        return final_score if final_score > 0 else 0

# Poor naming conventions (code smell)
def f(x, y, z):
    return x * y + z

def getData():
    return user_data

# Security issue: SQL injection vulnerability (code smell)
def get_user_by_id(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    # This would be vulnerable to SQL injection
    return query

# Dead code (code smell)
def unused_function():
    print("This function is never called")
    return "unused"

# Main execution with poor error handling
if __name__ == "__main__":
    processor = DataProcessor()
    
    # Hardcoded test data
    test_emails = ["john@example.com", "invalid-email", "test@domain.co.uk"]
    
    for email in test_emails:
        try:
            result = processor.process_user_data(email, "email", "json", True, True)
            print(f"Email {email}: {result}")
        except:
            print("Something went wrong")  # Poor error handling
    
    # More hardcoded values
    metrics = {"accuracy": 0.92, "response_time": 1500}
    score = processor.calculate_score(metrics)
    print(f"Final score: {score}")
'''

class BackendTester:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.test_results = []
        self.user_id = f"test_user_{uuid.uuid4().hex[:8]}"
        
    def log_test(self, test_name: str, success: bool, response_time: float, details: Dict[str, Any]):
        """Log test results"""
        self.test_results.append({
            "test_name": test_name,
            "success": success,
            "response_time_ms": round(response_time * 1000, 2),
            "details": details
        })
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name} ({response_time*1000:.2f}ms)")
        if not success:
            print(f"   Error: {details.get('error', 'Unknown error')}")
    
    def test_health_check(self):
        """Test 1: Health Check Endpoint"""
        print("\n🔍 Testing Health Check Endpoint...")
        
        try:
            start_time = time.time()
            response = requests.get(f"{self.base_url}/health", timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate response structure
                required_fields = ["status", "version", "ai_engine", "agents", "database", "features"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test("Health Check", False, response_time, {
                        "error": f"Missing fields: {missing_fields}",
                        "response": data
                    })
                else:
                    self.log_test("Health Check", True, response_time, {
                        "status": data["status"],
                        "version": data["version"],
                        "features_count": len(data["features"]),
                        "agents_status": data["agents"]
                    })
            else:
                self.log_test("Health Check", False, response_time, {
                    "error": f"HTTP {response.status_code}",
                    "response": response.text
                })
                
        except Exception as e:
            self.log_test("Health Check", False, 0, {"error": str(e)})
    
    def test_code_analysis_advanced(self):
        """Test 2: Advanced Code Analysis Endpoint"""
        print("\n🔍 Testing Advanced Code Analysis...")
        
        try:
            payload = {
                "code": PYTHON_CODE_WITH_SMELLS,
                "language": "python",
                "file_path": "test_analysis.py",
                "analysis_type": "comprehensive",
                "user_id": self.user_id,
                "include_smells": True,
                "include_complexity": True,
                "include_dependencies": True
            }
            
            start_time = time.time()
            response = requests.post(
                f"{self.base_url}/api/v2/analyze-code-advanced",
                json=payload,
                timeout=30
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate response structure
                expected_fields = ["success", "file_path", "language", "analysis_timestamp"]
                missing_fields = [field for field in expected_fields if field not in data]
                
                if missing_fields:
                    self.log_test("Advanced Code Analysis", False, response_time, {
                        "error": f"Missing fields: {missing_fields}",
                        "response": data
                    })
                else:
                    # Check for code smells detection
                    smells_detected = len(data.get("code_smells", []))
                    
                    self.log_test("Advanced Code Analysis", True, response_time, {
                        "success": data["success"],
                        "language": data["language"],
                        "smells_detected": smells_detected,
                        "has_ast_analysis": "ast_analysis" in data,
                        "has_smell_summary": "smell_summary" in data,
                        "analysis_id": data.get("analysis_id", "Not saved")
                    })
            else:
                self.log_test("Advanced Code Analysis", False, response_time, {
                    "error": f"HTTP {response.status_code}",
                    "response": response.text
                })
                
        except Exception as e:
            self.log_test("Advanced Code Analysis", False, 0, {"error": str(e)})
    
    def test_code_smell_detection(self):
        """Test 3: Code Smell Detection Endpoint"""
        print("\n🔍 Testing Code Smell Detection...")
        
        try:
            payload = {
                "code": PYTHON_CODE_WITH_SMELLS,
                "file_path": "test_smells.py",
                "language": "python",
                "user_id": self.user_id,
                "custom_rules": {
                    "max_function_length": 20,
                    "max_complexity": 10
                }
            }
            
            start_time = time.time()
            response = requests.post(
                f"{self.base_url}/api/v2/detect-code-smells",
                json=payload,
                timeout=20
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("success"):
                    smells = data.get("smells", [])
                    summary = data.get("summary", {})
                    
                    # Analyze detected smells
                    smell_types = [smell["type"] for smell in smells]
                    severity_counts = {}
                    for smell in smells:
                        severity = smell.get("severity", "unknown")
                        severity_counts[severity] = severity_counts.get(severity, 0) + 1
                    
                    self.log_test("Code Smell Detection", True, response_time, {
                        "total_smells": len(smells),
                        "smell_types": list(set(smell_types)),
                        "severity_distribution": severity_counts,
                        "has_summary": bool(summary),
                        "has_report": "report" in data
                    })
                else:
                    self.log_test("Code Smell Detection", False, response_time, {
                        "error": "API returned success: false",
                        "response": data
                    })
            else:
                self.log_test("Code Smell Detection", False, response_time, {
                    "error": f"HTTP {response.status_code}",
                    "response": response.text
                })
                
        except Exception as e:
            self.log_test("Code Smell Detection", False, 0, {"error": str(e)})
    
    def test_learning_system(self):
        """Test 4: Learning System Endpoint"""
        print("\n🔍 Testing Learning System...")
        
        try:
            # Test different learning types
            learning_tests = [
                {
                    "learning_type": "code_style",
                    "data": {
                        "code": "def clean_function():\n    return 'well_formatted'",
                        "file_path": "clean_code.py",
                        "language": "python"
                    }
                },
                {
                    "learning_type": "commit_pattern",
                    "data": {
                        "commits": [
                            {"message": "fix: resolve bug in user validation", "files": ["user.py"]},
                            {"message": "feat: add new authentication method", "files": ["auth.py"]}
                        ]
                    }
                },
                {
                    "learning_type": "debug_session",
                    "data": {
                        "session_id": "debug_001",
                        "errors_encountered": ["TypeError", "AttributeError"],
                        "resolution_time": 300,
                        "success": True
                    }
                }
            ]
            
            all_success = True
            total_time = 0
            results = []
            
            for test_case in learning_tests:
                payload = {
                    "user_id": self.user_id,
                    "learning_type": test_case["learning_type"],
                    "data": test_case["data"]
                }
                
                start_time = time.time()
                response = requests.post(
                    f"{self.base_url}/api/v2/learn-user-pattern",
                    json=payload,
                    timeout=15
                )
                response_time = time.time() - start_time
                total_time += response_time
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        results.append({
                            "learning_type": test_case["learning_type"],
                            "status": "success",
                            "response_time": response_time
                        })
                    else:
                        all_success = False
                        results.append({
                            "learning_type": test_case["learning_type"],
                            "status": "failed",
                            "error": data
                        })
                else:
                    all_success = False
                    results.append({
                        "learning_type": test_case["learning_type"],
                        "status": "http_error",
                        "error": f"HTTP {response.status_code}"
                    })
            
            self.log_test("Learning System", all_success, total_time, {
                "tests_run": len(learning_tests),
                "all_passed": all_success,
                "results": results
            })
                
        except Exception as e:
            self.log_test("Learning System", False, 0, {"error": str(e)})
    
    def test_personalized_recommendations(self):
        """Test 5: Personalized Recommendations Endpoint"""
        print("\n🔍 Testing Personalized Recommendations...")
        
        try:
            payload = {
                "user_id": self.user_id,
                "context": {
                    "current_language": "python",
                    "project_type": "web_application",
                    "experience_level": "intermediate",
                    "recent_errors": ["TypeError", "AttributeError"],
                    "code_style_preferences": {
                        "max_line_length": 88,
                        "prefer_type_hints": True
                    }
                }
            }
            
            start_time = time.time()
            response = requests.post(
                f"{self.base_url}/api/v2/get-personalized-recommendations",
                json=payload,
                timeout=15
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("success"):
                    recommendations = data.get("recommendations", {})
                    
                    self.log_test("Personalized Recommendations", True, response_time, {
                        "user_id": data["user_id"],
                        "personalized": data.get("personalized", False),
                        "recommendation_types": list(recommendations.keys()),
                        "has_style_suggestions": "style_suggestions" in recommendations,
                        "total_recommendations": sum(len(v) if isinstance(v, list) else 1 for v in recommendations.values())
                    })
                else:
                    self.log_test("Personalized Recommendations", False, response_time, {
                        "error": "API returned success: false",
                        "response": data
                    })
            else:
                self.log_test("Personalized Recommendations", False, response_time, {
                    "error": f"HTTP {response.status_code}",
                    "response": response.text
                })
                
        except Exception as e:
            self.log_test("Personalized Recommendations", False, 0, {"error": str(e)})
    
    def test_user_progress(self):
        """Test 6: User Learning Progress Endpoint"""
        print("\n🔍 Testing User Learning Progress...")
        
        try:
            start_time = time.time()
            response = requests.get(
                f"{self.base_url}/api/v2/user-learning-progress/{self.user_id}",
                timeout=10
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("success"):
                    progress = data.get("progress", {})
                    analytics = data.get("analytics", {})
                    
                    self.log_test("User Learning Progress", True, response_time, {
                        "user_id": data["user_id"],
                        "has_progress_data": bool(progress),
                        "has_analytics_data": bool(analytics),
                        "progress_keys": list(progress.keys()) if progress else [],
                        "analytics_keys": list(analytics.keys()) if analytics else []
                    })
                else:
                    self.log_test("User Learning Progress", False, response_time, {
                        "error": "API returned success: false",
                        "response": data
                    })
            else:
                self.log_test("User Learning Progress", False, response_time, {
                    "error": f"HTTP {response.status_code}",
                    "response": response.text
                })
                
        except Exception as e:
            self.log_test("User Learning Progress", False, 0, {"error": str(e)})
    
    def test_supported_languages(self):
        """Test 7: Supported Languages Endpoint"""
        print("\n🔍 Testing Supported Languages...")
        
        try:
            start_time = time.time()
            response = requests.get(
                f"{self.base_url}/api/v2/supported-languages",
                timeout=10
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("success"):
                    languages = data.get("languages", [])
                    
                    # Validate language structure
                    valid_languages = []
                    for lang in languages:
                        if all(key in lang for key in ["name", "code", "extensions", "features"]):
                            valid_languages.append(lang)
                    
                    self.log_test("Supported Languages", True, response_time, {
                        "total_languages": len(languages),
                        "valid_languages": len(valid_languages),
                        "language_codes": [lang["code"] for lang in valid_languages],
                        "python_supported": any(lang["code"] == "python" for lang in languages),
                        "javascript_supported": any(lang["code"] == "javascript" for lang in languages)
                    })
                else:
                    self.log_test("Supported Languages", False, response_time, {
                        "error": "API returned success: false",
                        "response": data
                    })
            else:
                self.log_test("Supported Languages", False, response_time, {
                    "error": f"HTTP {response.status_code}",
                    "response": response.text
                })
                
        except Exception as e:
            self.log_test("Supported Languages", False, 0, {"error": str(e)})
    
    def run_all_tests(self):
        """Run all backend tests"""
        print("🚀 Starting DevMind AI Backend Comprehensive Testing...")
        print(f"Backend URL: {self.base_url}")
        print(f"Test User ID: {self.user_id}")
        print("=" * 80)
        
        # Run all tests
        self.test_health_check()
        self.test_code_analysis_advanced()
        self.test_code_smell_detection()
        self.test_learning_system()
        self.test_personalized_recommendations()
        self.test_user_progress()
        self.test_supported_languages()
        
        # Generate summary
        self.generate_summary()
    
    def generate_summary(self):
        """Generate comprehensive test summary"""
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE TEST RESULTS SUMMARY")
        print("=" * 80)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        # Performance metrics
        response_times = [result["response_time_ms"] for result in self.test_results if result["response_time_ms"] > 0]
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            max_response_time = max(response_times)
            min_response_time = min(response_times)
            
            print(f"\n📈 PERFORMANCE METRICS:")
            print(f"Average Response Time: {avg_response_time:.2f}ms")
            print(f"Fastest Response: {min_response_time:.2f}ms")
            print(f"Slowest Response: {max_response_time:.2f}ms")
        
        # Detailed results
        print(f"\n📋 DETAILED RESULTS:")
        for result in self.test_results:
            status = "✅" if result["success"] else "❌"
            print(f"{status} {result['test_name']} - {result['response_time_ms']}ms")
            if not result["success"]:
                print(f"   Error: {result['details'].get('error', 'Unknown error')}")
        
        # Critical issues
        critical_failures = [r for r in self.test_results if not r["success"]]
        if critical_failures:
            print(f"\n🚨 CRITICAL ISSUES FOUND:")
            for failure in critical_failures:
                print(f"- {failure['test_name']}: {failure['details'].get('error', 'Unknown error')}")
        
        # Code analysis accuracy
        code_analysis_result = next((r for r in self.test_results if r["test_name"] == "Advanced Code Analysis"), None)
        smell_detection_result = next((r for r in self.test_results if r["test_name"] == "Code Smell Detection"), None)
        
        if code_analysis_result and code_analysis_result["success"]:
            smells_detected = code_analysis_result["details"].get("smells_detected", 0)
            print(f"\n🔍 CODE ANALYSIS ACCURACY:")
            print(f"Code Smells Detected: {smells_detected}")
            print(f"Expected Smells: 8+ (long methods, duplicates, hardcoded values, poor naming, etc.)")
            
        if smell_detection_result and smell_detection_result["success"]:
            total_smells = smell_detection_result["details"].get("total_smells", 0)
            smell_types = smell_detection_result["details"].get("smell_types", [])
            print(f"Dedicated Smell Detection: {total_smells} smells")
            print(f"Smell Types Found: {', '.join(smell_types)}")

if __name__ == "__main__":
    tester = BackendTester()
    tester.run_all_tests()