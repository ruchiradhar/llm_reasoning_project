#!/usr/bin/env python3
"""
Verification script to check project integrity.
Run this to ensure all components are properly set up.
"""

import sys
import os
from pathlib import Path

def check_files():
    """Check if all required files exist"""
    required_files = [
        "README.md",
        "QUICKSTART.md",
        "ARCHITECTURE.md",
        "CONTRIBUTING.md",
        "PROJECT_SUMMARY.md",
        "requirements.txt",
        "setup.py",
        ".gitignore",
        "benchmark.py",
        "examples.py",
        "src/__init__.py",
        "src/model_loader.py",
        "src/evaluator.py",
        "tasks/__init__.py",
        "tasks/math_reasoning.py",
        "tasks/logic_reasoning.py",
    ]
    
    print("Checking project files...")
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} - MISSING")
            all_exist = False
    
    return all_exist

def check_imports():
    """Check if core modules can be imported"""
    print("\nChecking Python imports...")
    
    try:
        sys.path.insert(0, os.getcwd())
        
        # Try importing core modules
        from src.model_loader import ModelLoader
        print("  ✓ ModelLoader")
        
        from src.evaluator import Evaluator
        print("  ✓ Evaluator")
        
        from tasks.math_reasoning import MathReasoningTask
        print("  ✓ MathReasoningTask")
        
        from tasks.logic_reasoning import LogicReasoningTask
        print("  ✓ LogicReasoningTask")
        
        return True
        
    except ImportError as e:
        print(f"  ✗ Import error: {e}")
        return False

def check_dependencies():
    """Check if dependencies are listed"""
    print("\nChecking dependencies...")
    
    required_deps = [
        "torch", "transformers", "huggingface-hub",
        "numpy", "pandas", "tabulate", "tqdm"
    ]
    
    try:
        with open("requirements.txt", "r") as f:
            content = f.read()
            
        all_present = True
        for dep in required_deps:
            if dep in content:
                print(f"  ✓ {dep}")
            else:
                print(f"  ✗ {dep} - MISSING")
                all_present = False
        
        return all_present
        
    except FileNotFoundError:
        print("  ✗ requirements.txt not found")
        return False

def count_lines():
    """Count lines of code"""
    print("\nCounting lines of code...")
    
    python_files = [
        "benchmark.py",
        "examples.py",
        "src/model_loader.py",
        "src/evaluator.py",
        "tasks/math_reasoning.py",
        "tasks/logic_reasoning.py",
    ]
    
    total_lines = 0
    for file in python_files:
        if os.path.exists(file):
            with open(file, "r") as f:
                lines = len(f.readlines())
                total_lines += lines
                print(f"  {file}: {lines} lines")
    
    print(f"\n  Total: {total_lines} lines of Python code")
    return total_lines

def main():
    """Run all verification checks"""
    print("="*70)
    print("LLM REASONING BENCHMARK - PROJECT VERIFICATION")
    print("="*70)
    print()
    
    checks = []
    
    # Run checks
    checks.append(("Files", check_files()))
    checks.append(("Dependencies", check_dependencies()))
    checks.append(("Imports", check_imports()))
    
    # Count lines
    count_lines()
    
    # Summary
    print("\n" + "="*70)
    print("VERIFICATION SUMMARY")
    print("="*70)
    
    all_passed = True
    for name, passed in checks:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{name}: {status}")
        if not passed:
            all_passed = False
    
    print("="*70)
    
    if all_passed:
        print("\n✓ All checks passed! Project is ready to use.")
        print("\nNext steps:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Run benchmark: python benchmark.py")
        print("  3. Check results: cat results/leaderboard_latest.csv")
        return 0
    else:
        print("\n✗ Some checks failed. Please review errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
