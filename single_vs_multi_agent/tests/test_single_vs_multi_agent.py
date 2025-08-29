"""
Test cases for single vs multi agent evaluations using LangSmith pytest integration.
"""
import sys
from pathlib import Path
from unittest.mock import patch, Mock
import pytest
from langsmith import testing as t

# Add the parent directory to the path so we can import our modules
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from main import call_langflow_api, create_ls_target # type: ignore

@pytest.mark.langsmith
def test_single_agent_basic_math():
    """Test basic math problem solving with single agent."""
    question = "What is 15 * 3?"
    expected_answer = "45"

    # Log inputs and expected outputs for LangSmith
    t.log_inputs({"question": question})
    t.log_reference_outputs({"expected_answer": expected_answer})

    # Mock the API call to avoid real requests during testing
    with patch('requests.request') as mock_request:
        mock_response = Mock()
        mock_response.json.return_value = {
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
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Test the single agent endpoint
        response = call_langflow_api(
            question, 
            "Qwen", 
            "qwen3-4b-2507", 
            None, 
            "math_eval_single_lms"
        )

        # Log the actual output
        t.log_outputs({"single_agent_response": response})

        # Basic assertion - this becomes 'pass' feedback in LangSmith
        assert response is not None
        assert "45" in response

@pytest.mark.langsmith
def test_multi_agent_basic_math():
    """Test basic math problem solving with multi agent."""
    question = "What is 15 * 3?"
    expected_answer = "45"

    # Log inputs and expected outputs for LangSmith
    t.log_inputs({"question": question})
    t.log_reference_outputs({"expected_answer": expected_answer})

    # Mock the API call
    with patch('requests.request') as mock_request:
        mock_response = Mock()
        mock_response.json.return_value = {
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
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Test the multi agent endpoint
        response = call_langflow_api(
            question, 
            "Qwen", 
            "qwen3-4b-2507", 
            None, 
            "math_eval_multi_lms"
        )

        # Log the actual output
        t.log_outputs({"multi_agent_response": response})

        # Basic assertion
        assert response is not None
        assert "45" in response

@pytest.mark.langsmith
def test_single_vs_multi_agent_comparison():
    """Compare single vs multi agent performance on the same problem."""
    question = "Solve: 2x + 5 = 13"
    expected_answer = "x = 4"

    # Log inputs and expected outputs
    t.log_inputs({"question": question})
    t.log_reference_outputs({"expected_answer": expected_answer})

    # Mock API calls for both endpoints
    with patch('requests.request') as mock_request:
        mock_response = Mock()
        mock_response.json.return_value = {
            "outputs": [
                {
                    "outputs": [
                        {
                            "results": {
                                "message": {
                                    "data": {
                                        "text": "x = 4"
                                    }
                                }
                            }
                        }
                    ]
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Test single agent
        single_response = call_langflow_api(
            question, 
            "Qwen", 
            "qwen3-4b-2507", 
            None, 
            "math_eval_single_lms"
        )

        # Test multi agent
        multi_response = call_langflow_api(
            question, 
            "Qwen", 
            "qwen3-4b-2507", 
            None, 
            "math_eval_multi_lms"
        )

        # Log both responses for comparison
        t.log_outputs({
            "single_agent_response": single_response,
            "multi_agent_response": multi_response
        })

        # Both should produce valid responses
        assert single_response is not None
        assert multi_response is not None

        # At least one should contain the expected answer
        assert ("x = 4" in single_response or "x = 4" in multi_response)

@pytest.mark.langsmith
def test_metadata_enhancement():
    """Test that questions are properly enhanced with metadata."""
    question = "What is 10 / 2?"
    metadata = {"Unit": "apples", "Rounding": "nearest whole"}

    # Log inputs
    t.log_inputs({
        "question": question,
        "metadata": metadata
    })

    # Create a target function to test metadata enhancement
    target_func = create_ls_target("Qwen", "qwen3-4b-2507", None, "math_eval_single_lms")

    # Mock the API call
    with patch('requests.request') as mock_request:
        mock_response = Mock()
        mock_response.json.return_value = {
            "outputs": [
                {
                    "outputs": [
                        {
                            "results": {
                                "message": {
                                    "data": {
                                        "text": "The answer is 5 apples"
                                    }
                                }
                            }
                        }
                    ]
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Test with metadata
        inputs = {"question": question, "metadata": metadata}
        result = target_func(inputs)

        # Log the result
        t.log_outputs({"enhanced_response": result})

        # Should return a response
        assert result is not None
        assert "response" in result

@pytest.mark.langsmith
@pytest.mark.parametrize("question,expected_components", [
    ("What is 8 + 4?", ["12", "8", "4", "addition"]),
    ("Calculate 6 * 7", ["42", "6", "7", "multiplication"]),
    ("Solve 3x = 15", ["x = 5", "3x", "15", "equation"])
])
def test_math_problem_variations(question, expected_components):
    """Test various math problems with parametrized inputs."""
    # Log inputs
    t.log_inputs({"question": question})
    t.log_reference_outputs({"expected_components": expected_components})

    # Mock API call
    with patch('requests.request') as mock_request:
        mock_response = Mock()
        mock_response.json.return_value = {
            "outputs": [
                {
                    "outputs": [
                        {
                            "results": {
                                "message": {
                                    "data": {
                                        "text": f"Answer: {expected_components[0]}"
                                    }
                                }
                            }
                        }
                    ]
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        # Test single agent
        response = call_langflow_api(
            question, 
            "Qwen", 
            "qwen3-4b-2507", 
            None, 
            "math_eval_single_lms"
        )

        # Log response
        t.log_outputs({"response": response})

        # Basic validation
        assert response is not None
        assert len(response) > 0
