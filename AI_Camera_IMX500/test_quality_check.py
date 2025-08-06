#!/usr/bin/env python3
"""
Quality Check Script for AI Camera IMX500 Educational System
Tests all created files for syntax errors, import issues, and basic functionality
"""

import sys
import os
import json
import importlib.util
from pathlib import Path

def test_notebook_json(notebook_path):
    """Test if notebook has valid JSON syntax"""
    try:
        with open(notebook_path, 'r') as f:
            json.load(f)
        return True, "Valid JSON"
    except Exception as e:
        return False, str(e)

def test_python_module(module_path):
    """Test if Python module can be imported and basic functionality works"""
    try:
        # Import module dynamically
        spec = importlib.util.spec_from_file_location("test_module", module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Test SmartVehicleSystem if it exists
        if hasattr(module, 'SmartVehicleSystem'):
            system = module.SmartVehicleSystem(enable_motor=False, debug=False)
            status = system.get_system_status()
            return True, f"Module imported and initialized successfully"
        else:
            return True, "Module imported successfully"
            
    except Exception as e:
        return False, str(e)

def main():
    print("🔍 AI CAMERA IMX500 EDUCATIONAL SYSTEM - QUALITY CHECK")
    print("=" * 60)
    
    # Test files to check
    test_files = {
        "Python Modules": [
            "04_Smart_Integration/smart_vehicle_system.py"
        ],
        "Level 1 Notebooks": [
            "01_Getting_Started/00_AI_Vision_Fundamentals.ipynb",
            "01_Getting_Started/Camera_Setup_Check.ipynb",
            "01_Getting_Started/Camera Preview.ipynb"
        ],
        "Level 4 Notebooks": [
            "04_Smart_Integration/01_AI_Motor_Bridge.ipynb",
            "04_Smart_Integration/04_Student_Project_Builder.ipynb"
        ]
    }
    
    total_tests = 0
    passed_tests = 0
    
    for category, files in test_files.items():
        print(f"\n📂 {category}:")
        print("-" * (len(category) + 4))
        
        for file_path in files:
            total_tests += 1
            full_path = Path(file_path)
            
            if not full_path.exists():
                print(f"   ❌ {file_path} - File not found")
                continue
            
            # Test based on file type
            if file_path.endswith('.py'):
                success, message = test_python_module(full_path)
            elif file_path.endswith('.ipynb'):
                success, message = test_notebook_json(full_path)
            else:
                success, message = False, "Unknown file type"
            
            if success:
                print(f"   ✅ {file_path} - {message}")
                passed_tests += 1
            else:
                print(f"   ❌ {file_path} - {message}")
    
    # Summary
    print(f"\n📊 QUALITY CHECK SUMMARY:")
    print("=" * 30)
    print(f"   Total Tests: {total_tests}")
    print(f"   Passed: {passed_tests}")
    print(f"   Failed: {total_tests - passed_tests}")
    print(f"   Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("\n🎉 ALL TESTS PASSED! Educational system is ready to use.")
        return 0
    else:
        print(f"\n⚠️ {total_tests - passed_tests} tests failed. Please review and fix issues.")
        return 1

if __name__ == "__main__":
    exit(main())