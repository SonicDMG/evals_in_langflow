"""
Shared pytest configuration and fixtures for single vs multi agent tests.
"""
import os
import pytest
from dotenv import load_dotenv

# Load environment variables from the root .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

@pytest.fixture
def mock_langflow_response():
    """Mock response from Langflow API."""
    return {
        "outputs": [
            {
                "outputs": [
                    {
                        "results": {
                            "message": {
                                "data": {
                                    "text": "The answer is 45"
                                }
                            }
                        }
                    }
                ]
            }
        ]
    }

@pytest.fixture
def sample_math_questions():
    """Sample math questions for testing."""
    return [
        {
            "question": "What is 15 * 3?",
            "expected_answer": "45",
            "expected_components": ["45", "15", "3", "multiplication"]
        },
        {
            "question": "Solve: 2x + 5 = 13",
            "expected_answer": "x = 4",
            "expected_components": ["x = 4", "2x", "5", "13", "equation"]
        }
    ]

@pytest.fixture
def model_config():
    """Sample model configuration for testing."""
    return {
        "provider": "Qwen",
        "model_name": "qwen3-4b-2507",
        "api_key": None
    }
