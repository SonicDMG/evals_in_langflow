#!/usr/bin/env python3
"""
Quick test script to validate the pytest setup.
Run this to check if everything is configured correctly.
"""
import sys
import os
from pathlib import Path

def test_imports():
    """Test that we can import the required modules."""
    print("🧪 Testing imports...")

    try:
        import pytest
        print("✅ pytest imported successfully")
    except ImportError:
        print("❌ pytest not found. Install with: pip install -r requirements.txt")
        return False

    try:
        from langsmith import testing
        print("✅ langsmith.testing imported successfully")
    except ImportError:
        print("❌ langsmith[pytest] not found. Install with: pip install -r requirements.txt")
        return False

    try:
        # Add parent to path and import our modules
        sys.path.insert(0, str(Path(__file__).parent))
        from main import call_langflow_api, create_ls_target
        print("✅ Local modules imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import local modules: {e}")
        return False

    return True

def test_environment():
    """Test environment configuration."""
    print("\n🔧 Testing environment...")

    # Check for required environment variables
    required_vars = ['LANGCHAIN_API_KEY', 'LANGFLOW_API_KEY']
    missing_vars = []

    for var in required_vars:
        if os.getenv(var):
            print(f"✅ {var} is set")
        else:
            print(f"❌ {var} is not set")
            missing_vars.append(var)

    if missing_vars:
        print(f"\n⚠️  Missing environment variables: {', '.join(missing_vars)}")
        print("   Make sure your .env file is configured correctly")
        return False

    return True

def test_directory_structure():
    """Test that the directory structure is correct."""
    print("\n📁 Testing directory structure...")

    current_dir = Path(__file__).parent
    required_files = [
        'main.py',
        'config.py',
        'requirements.txt',
        'tests/test_single_vs_multi_agent.py'
    ]

    missing_files = []
    for file_path in required_files:
        full_path = current_dir / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)

    if missing_files:
        print(f"\n⚠️  Missing files: {', '.join(missing_files)}")
        return False

    return True

def main():
    """Run all validation tests."""
    print("🚀 Single vs Multi Agent - Quick Validation Test")
    print("=" * 50)

    tests = [
        test_imports,
        test_environment,
        test_directory_structure
    ]

    all_passed = True
    for test in tests:
        if not test():
            all_passed = False

    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All validation tests passed!")
        print("\nNext steps:")
        print("1. Run: pytest tests/ --langsmith-output")
        print("2. Check LangSmith for your test results")
        print("3. Add your real datasets to the test files")
    else:
        print("❌ Some validation tests failed.")
        print("Please fix the issues above before running the full test suite.")

    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

