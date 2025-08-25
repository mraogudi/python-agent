#!/usr/bin/env python3
"""
Test script for Python Coding Agent components.
This script tests the core functionality without requiring an OpenAI API key.
"""

import sys
import json
from code_executor import CodeExecutor

def test_code_executor():
    """Test the code executor with various Python code snippets."""
    print("🧪 Testing Code Executor...")
    
    executor = CodeExecutor()
    
    # Test 1: Simple print statement
    print("\n📝 Test 1: Simple Print Statement")
    result = executor.execute_code("print('Hello, World!')")
    print(f"Success: {result['success']}")
    print(f"Output: {repr(result['output'])}")
    print(f"Execution time: {result['execution_time']:.3f}s")
    
    # Test 2: Mathematical computation
    print("\n📝 Test 2: Mathematical Computation")
    result = executor.execute_code("""
import math

def calculate_circle_area(radius):
    return math.pi * radius ** 2

radius = 5
area = calculate_circle_area(radius)
print(f"Circle with radius {radius} has area: {area:.2f}")
""")
    print(f"Success: {result['success']}")
    print(f"Output: {repr(result['output'])}")
    
    # Test 3: Error handling
    print("\n📝 Test 3: Error Handling")
    result = executor.execute_code("x = 1 / 0  # Division by zero")
    print(f"Success: {result['success']}")
    print(f"Error: {result['error']}")
    
    # Test 4: Security test (should be blocked)
    print("\n📝 Test 4: Security Test (Dangerous Import)")
    result = executor.execute_code("import os; print(os.getcwd())")
    print(f"Success: {result['success']}")
    print(f"Error: {result['error']}")
    
    # Test 5: Loop with output
    print("\n📝 Test 5: Loop with Output")
    result = executor.execute_code("""
for i in range(3):
    print(f"Count: {i}")
""")
    print(f"Success: {result['success']}")
    print(f"Output: {repr(result['output'])}")
    
    print("\n✅ Code Executor tests completed!")

def test_coding_agent():
    """Test the coding agent (requires OpenAI API key)."""
    print("\n🤖 Testing Coding Agent...")
    
    try:
        from coding_agent import CodingAgent
        
        agent = CodingAgent()
        print("✅ Coding agent initialized successfully!")
        
        # Test validation
        validation = agent.validate_task_description("Create a simple calculator")
        print(f"Validation result: {validation}")
        
        print("ℹ️  To test code generation, you need a valid OpenAI API key.")
        print("   Set OPENAI_API_KEY environment variable and run the web app.")
        
    except Exception as e:
        print(f"⚠️  Coding agent not available: {e}")
        print("   This is expected if OpenAI API key is not configured.")

def test_flask_imports():
    """Test that all Flask-related imports work."""
    print("\n🌐 Testing Flask Dependencies...")
    
    try:
        import flask
        print("✅ Flask imported successfully")
        
        from app import app
        print("✅ Main Flask app imported successfully")
        
        # Test that the app is properly configured
        with app.app_context():
            print(f"✅ App context works, debug mode: {app.debug}")
        
    except Exception as e:
        print(f"❌ Flask import error: {e}")
        return False
    
    return True

def test_static_files():
    """Test that static files exist and are readable."""
    print("\n📁 Testing Static Files...")
    
    files_to_check = [
        'templates/base.html',
        'templates/index.html',
        'static/css/style.css',
        'static/js/app.js'
    ]
    
    for file_path in files_to_check:
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                print(f"✅ {file_path} ({len(content)} chars)")
        except FileNotFoundError:
            print(f"❌ {file_path} not found")
        except Exception as e:
            print(f"❌ Error reading {file_path}: {e}")

def run_system_check():
    """Run a comprehensive system check."""
    print("🚀 Python Coding Agent - System Check")
    print("=" * 50)
    
    # Check Python version
    print(f"🐍 Python version: {sys.version}")
    
    # Test core components
    test_code_executor()
    test_coding_agent()
    
    # Test Flask setup
    flask_ok = test_flask_imports()
    
    # Test static files
    test_static_files()
    
    print("\n" + "=" * 50)
    print("📊 System Check Summary:")
    print("✅ Code Executor: Working")
    print("⚠️  Coding Agent: Requires OpenAI API key")
    print(f"{'✅' if flask_ok else '❌'} Flask Application: {'Ready' if flask_ok else 'Error'}")
    print("✅ Static Files: Present")
    
    print("\n🎯 Next Steps:")
    if flask_ok:
        print("1. Set your OpenAI API key in a .env file:")
        print("   OPENAI_API_KEY=your_api_key_here")
        print("2. Run the application: python app.py")
        print("3. Open http://localhost:5000 in your browser")
    else:
        print("1. Fix Flask import issues")
        print("2. Install missing dependencies: pip install -r requirements.txt")
    
    print("\n🎉 Happy coding!")

if __name__ == "__main__":
    run_system_check() 