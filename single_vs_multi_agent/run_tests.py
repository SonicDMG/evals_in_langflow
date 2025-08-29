#!/usr/bin/env python3
"""
Test runner script for single vs multi agent evaluations.
This script sets up the environment and runs pytest with LangSmith integration.
"""
import os
import sys
import subprocess
from pathlib import Path

def setup_environment():
    """Set up environment variables for testing."""
    # Set test suite name for LangSmith
    os.environ['LANGSMITH_TEST_SUITE'] = 'Single vs Multi Agent Evaluation'

    # Set experiment name
    os.environ['LANGSMITH_EXPERIMENT'] = 'pytest-evaluation'

    # Enable test tracking (set to 'false' to disable)
    os.environ['LANGSMITH_TEST_TRACKING'] = 'true'

    # Optional: Set cache directory for expensive API calls
    cache_dir = Path(__file__).parent / 'test_cache'
    cache_dir.mkdir(exist_ok=True)
    os.environ['LANGSMITH_TEST_CACHE'] = str(cache_dir)

    print("✅ Environment configured:")
    print(f"   Test Suite: {os.environ['LANGSMITH_TEST_SUITE']}")
    print(f"   Experiment: {os.environ['LANGSMITH_EXPERIMENT']}")
    print(f"   Cache Dir: {os.environ['LANGSMITH_TEST_CACHE']}")

def run_tests():
    """Run the pytest tests."""
    print("\n🚀 Starting pytest with LangSmith integration...")

    # Get the tests directory
    tests_dir = Path(__file__).parent / 'tests'

    # Build pytest command
    cmd = [
        sys.executable, '-m', 'pytest',
        str(tests_dir),
        '-v',  # Verbose output
        '--tb=short',  # Short traceback format
        '--cache-clear'  # Clear cache for fresh run
    ]

    print(f"Running: {' '.join(cmd)}")

    try:
        # Run pytest
        result = subprocess.run(cmd, cwd=Path(__file__).parent, check=True)
        print("\n✅ Tests completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Tests failed with exit code {e.returncode}")
        return False
    except FileNotFoundError:
        print("\n❌ pytest not found. Please install it first:")
        print("   pip install -r requirements.txt")
        return False

def main():
    """Main function."""
    print("🧪 Single vs Multi Agent Evaluation Test Runner")
    print("=" * 50)

    # Check if we're in the right directory
    if not Path(__file__).parent.exists():
        print("❌ Error: Cannot find tests directory")
        return False

    # Setup environment
    setup_environment()

    # Run tests
    success = run_tests()

    if success:
        print("\n🎉 All tests passed! Check LangSmith for detailed results.")
        print("\n💡 Tips:")
        print("   - Set LANGSMITH_TEST_TRACKING=false to run without LangSmith")
        print("   - Use --no-langsmith-output for standard pytest output")
        print("   - Check the test_cache directory for cached API responses")
    else:
        print("\n🔧 Troubleshooting:")
        print("   - Ensure all dependencies are installed: pip install -r requirements.txt")
        print("   - Check that your .env file has the required API keys")
        print("   - Verify that pytest is available in your environment")

    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
