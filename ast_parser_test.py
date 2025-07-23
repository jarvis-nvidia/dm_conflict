#!/usr/bin/env python3
"""
Focused AST Parser Testing
Tests the specific AST parser methods mentioned in the review request
"""

import requests
import json
import time

# Backend URL
BACKEND_URL = "https://9e1b2eda-fb7f-47df-b042-a0aaf5a14807.preview.emergentagent.com"

# Sample Python code to test AST parsing
PYTHON_TEST_CODE = '''
import os
import sys
from datetime import datetime

# Global variables
user_count = 0
config_data = {"api_key": "test123", "timeout": 30}
DEBUG_MODE = True

class DataProcessor:
    def __init__(self):
        self.data = []
        
    def process_data(self, input_data, validation_type="strict", debug=False):
        """Process input data with validation"""
        if validation_type == "strict":
            if not input_data:
                return False
            if len(input_data) < 5:
                return False
            return True
        elif validation_type == "loose":
            return bool(input_data)
        else:
            return None
    
    def calculate_metrics(self, data):
        if len(data) > 100:
            complexity = 10
        elif len(data) > 50:
            complexity = 5
        else:
            complexity = 1
        return complexity

def helper_function(x, y):
    return x + y

def main():
    processor = DataProcessor()
    result = processor.process_data("test data", "strict", True)
    print(f"Result: {result}")
'''

# JavaScript test code
JAVASCRIPT_TEST_CODE = '''
import React from 'react';
import { useState, useEffect } from 'react';

const DataProcessor = () => {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(false);
    
    const processData = (inputData, validationType = 'strict') => {
        if (validationType === 'strict') {
            if (!inputData || inputData.length < 5) {
                return false;
            }
            return true;
        } else if (validationType === 'loose') {
            return Boolean(inputData);
        }
        return null;
    };
    
    const calculateComplexity = (data) => {
        if (data.length > 100) {
            return 10;
        } else if (data.length > 50) {
            return 5;
        } else {
            return 1;
        }
    };
    
    useEffect(() => {
        setLoading(true);
        // Simulate data loading
        setTimeout(() => {
            setData(['item1', 'item2', 'item3']);
            setLoading(false);
        }, 1000);
    }, []);
    
    return (
        <div>
            <h1>Data Processor</h1>
            {loading ? <p>Loading...</p> : <p>Data loaded: {data.length} items</p>}
        </div>
    );
};

export default DataProcessor;
'''

# TypeScript test code
TYPESCRIPT_TEST_CODE = '''
interface User {
    id: number;
    name: string;
    email: string;
    isActive: boolean;
}

type UserRole = 'admin' | 'user' | 'guest';

enum Status {
    PENDING = 'pending',
    APPROVED = 'approved',
    REJECTED = 'rejected'
}

class UserManager {
    private users: User[] = [];
    
    constructor(private apiUrl: string) {}
    
    public addUser(user: User): boolean {
        if (this.validateUser(user)) {
            this.users.push(user);
            return true;
        }
        return false;
    }
    
    private validateUser(user: User): boolean {
        if (!user.name || !user.email) {
            return false;
        }
        if (user.name.length < 2) {
            return false;
        }
        if (!user.email.includes('@')) {
            return false;
        }
        return true;
    }
    
    public getUsersByRole(role: UserRole): User[] {
        return this.users.filter(user => user.isActive);
    }
    
    public getStatus(): Status {
        return Status.PENDING;
    }
}

function processUsers(users: User[], callback: (user: User) => void): void {
    users.forEach(callback);
}

export { User, UserRole, Status, UserManager, processUsers };
'''

class ASTParserTester:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.user_id = "demo_user"
        self.test_results = []
        
    def log_test(self, test_name: str, success: bool, response_time: float, details: dict):
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
        else:
            print(f"   Details: {details}")
    
    def test_python_ast_parsing(self):
        """Test Python AST parsing with focus on _extract_python_globals method"""
        print("\n🔍 Testing Python AST Parsing (including _extract_python_globals)...")
        
        try:
            payload = {
                "code": PYTHON_TEST_CODE,
                "language": "python",
                "file_path": "test_python.py",
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
                
                if data.get("success"):
                    ast_analysis = data.get("ast_analysis", {})
                    
                    # Check for Python-specific AST features
                    has_globals = "globals" in ast_analysis
                    has_imports = "imports" in ast_analysis
                    has_functions = "functions" in ast_analysis
                    has_classes = "classes" in ast_analysis
                    
                    # Check globals extraction specifically
                    globals_found = ast_analysis.get("globals", [])
                    expected_globals = ["user_count", "config_data", "DEBUG_MODE"]
                    globals_match = any(g in str(globals_found) for g in expected_globals)
                    
                    self.log_test("Python AST Parsing", True, response_time, {
                        "has_ast_analysis": bool(ast_analysis),
                        "has_globals": has_globals,
                        "has_imports": has_imports,
                        "has_functions": has_functions,
                        "has_classes": has_classes,
                        "globals_found": globals_found,
                        "globals_extraction_working": globals_match,
                        "functions_count": len(ast_analysis.get("functions", [])),
                        "classes_count": len(ast_analysis.get("classes", [])),
                        "imports_count": len(ast_analysis.get("imports", []))
                    })
                else:
                    self.log_test("Python AST Parsing", False, response_time, {
                        "error": "API returned success: false",
                        "response": data
                    })
            else:
                self.log_test("Python AST Parsing", False, response_time, {
                    "error": f"HTTP {response.status_code}",
                    "response": response.text[:500]
                })
                
        except Exception as e:
            self.log_test("Python AST Parsing", False, 0, {"error": str(e)})
    
    def test_javascript_ast_parsing(self):
        """Test JavaScript AST parsing with focus on _calculate_js_complexity method"""
        print("\n🔍 Testing JavaScript AST Parsing (including _calculate_js_complexity)...")
        
        try:
            payload = {
                "code": JAVASCRIPT_TEST_CODE,
                "language": "javascript",
                "file_path": "test_javascript.js",
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
                
                if data.get("success"):
                    ast_analysis = data.get("ast_analysis", {})
                    
                    # Check for JavaScript-specific AST features
                    has_functions = "functions" in ast_analysis
                    has_imports = "imports" in ast_analysis
                    has_exports = "exports" in ast_analysis
                    
                    # Check complexity calculation
                    functions = ast_analysis.get("functions", [])
                    complexity_calculated = any(func.get("complexity", 0) > 0 for func in functions)
                    
                    self.log_test("JavaScript AST Parsing", True, response_time, {
                        "has_ast_analysis": bool(ast_analysis),
                        "has_functions": has_functions,
                        "has_imports": has_imports,
                        "has_exports": has_exports,
                        "functions_count": len(functions),
                        "complexity_calculated": complexity_calculated,
                        "js_complexity_working": complexity_calculated,
                        "imports_found": ast_analysis.get("imports", []),
                        "exports_found": ast_analysis.get("exports", [])
                    })
                else:
                    self.log_test("JavaScript AST Parsing", False, response_time, {
                        "error": "API returned success: false",
                        "response": data
                    })
            else:
                self.log_test("JavaScript AST Parsing", False, response_time, {
                    "error": f"HTTP {response.status_code}",
                    "response": response.text[:500]
                })
                
        except Exception as e:
            self.log_test("JavaScript AST Parsing", False, 0, {"error": str(e)})
    
    def test_typescript_ast_parsing(self):
        """Test TypeScript AST parsing with focus on _extract_typescript_types method"""
        print("\n🔍 Testing TypeScript AST Parsing (including _extract_typescript_types)...")
        
        try:
            payload = {
                "code": TYPESCRIPT_TEST_CODE,
                "language": "typescript",
                "file_path": "test_typescript.ts",
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
                
                if data.get("success"):
                    ast_analysis = data.get("ast_analysis", {})
                    
                    # Check for TypeScript-specific AST features
                    has_types = "types" in ast_analysis
                    has_functions = "functions" in ast_analysis
                    has_classes = "classes" in ast_analysis
                    
                    # Check types extraction specifically
                    types_found = ast_analysis.get("types", [])
                    expected_types = ["User", "UserRole", "Status", "UserManager"]
                    types_match = any(t in types_found for t in expected_types)
                    
                    self.log_test("TypeScript AST Parsing", True, response_time, {
                        "has_ast_analysis": bool(ast_analysis),
                        "has_types": has_types,
                        "has_functions": has_functions,
                        "has_classes": has_classes,
                        "types_found": types_found,
                        "types_extraction_working": types_match,
                        "typescript_types_working": types_match,
                        "functions_count": len(ast_analysis.get("functions", [])),
                        "classes_count": len(ast_analysis.get("classes", []))
                    })
                else:
                    self.log_test("TypeScript AST Parsing", False, response_time, {
                        "error": "API returned success: false",
                        "response": data
                    })
            else:
                self.log_test("TypeScript AST Parsing", False, response_time, {
                    "error": f"HTTP {response.status_code}",
                    "response": response.text[:500]
                })
                
        except Exception as e:
            self.log_test("TypeScript AST Parsing", False, 0, {"error": str(e)})
    
    def test_endpoint_availability(self):
        """Test that the /api/v2/analyze-code-advanced endpoint is available"""
        print("\n🔍 Testing Advanced Code Analysis Endpoint Availability...")
        
        try:
            # Simple test with minimal payload
            payload = {
                "code": "def hello(): return 'world'",
                "language": "python",
                "user_id": self.user_id
            }
            
            start_time = time.time()
            response = requests.post(
                f"{self.base_url}/api/v2/analyze-code-advanced",
                json=payload,
                timeout=15
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("Endpoint Availability", True, response_time, {
                    "status_code": response.status_code,
                    "response_success": data.get("success", False),
                    "endpoint_working": True
                })
            else:
                self.log_test("Endpoint Availability", False, response_time, {
                    "status_code": response.status_code,
                    "error": f"HTTP {response.status_code}",
                    "response": response.text[:200]
                })
                
        except Exception as e:
            self.log_test("Endpoint Availability", False, 0, {"error": str(e)})
    
    def run_all_tests(self):
        """Run all AST parser tests"""
        print("🚀 Starting AST Parser Focused Testing...")
        print(f"Backend URL: {self.base_url}")
        print(f"Test User ID: {self.user_id}")
        print("=" * 80)
        
        # Run all tests
        self.test_endpoint_availability()
        self.test_python_ast_parsing()
        self.test_javascript_ast_parsing()
        self.test_typescript_ast_parsing()
        
        # Generate summary
        self.generate_summary()
    
    def generate_summary(self):
        """Generate test summary"""
        print("\n" + "=" * 80)
        print("📊 AST PARSER TEST RESULTS SUMMARY")
        print("=" * 80)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        # Detailed results
        print(f"\n📋 DETAILED RESULTS:")
        for result in self.test_results:
            status = "✅" if result["success"] else "❌"
            print(f"{status} {result['test_name']} - {result['response_time_ms']}ms")
            if not result["success"]:
                print(f"   Error: {result['details'].get('error', 'Unknown error')}")
        
        # Method-specific verification
        print(f"\n🔍 METHOD VERIFICATION:")
        
        python_test = next((r for r in self.test_results if r["test_name"] == "Python AST Parsing"), None)
        if python_test and python_test["success"]:
            globals_working = python_test["details"].get("globals_extraction_working", False)
            print(f"✅ _extract_python_globals method: {'WORKING' if globals_working else 'NOT WORKING'}")
        else:
            print("❌ _extract_python_globals method: FAILED TO TEST")
        
        js_test = next((r for r in self.test_results if r["test_name"] == "JavaScript AST Parsing"), None)
        if js_test and js_test["success"]:
            complexity_working = js_test["details"].get("js_complexity_working", False)
            print(f"✅ _calculate_js_complexity method: {'WORKING' if complexity_working else 'NOT WORKING'}")
        else:
            print("❌ _calculate_js_complexity method: FAILED TO TEST")
        
        ts_test = next((r for r in self.test_results if r["test_name"] == "TypeScript AST Parsing"), None)
        if ts_test and ts_test["success"]:
            types_working = ts_test["details"].get("typescript_types_working", False)
            print(f"✅ _extract_typescript_types method: {'WORKING' if types_working else 'NOT WORKING'}")
        else:
            print("❌ _extract_typescript_types method: FAILED TO TEST")
        
        endpoint_test = next((r for r in self.test_results if r["test_name"] == "Endpoint Availability"), None)
        if endpoint_test and endpoint_test["success"]:
            print("✅ /api/v2/analyze-code-advanced endpoint: WORKING (HTTP 200)")
        else:
            print("❌ /api/v2/analyze-code-advanced endpoint: FAILED")

if __name__ == "__main__":
    tester = ASTParserTester()
    tester.run_all_tests()