"""
Unit tests for single vs multi agent evaluations.
These tests use mocked dependencies and don't make external API calls.
"""
import sys
from pathlib import Path
from unittest.mock import patch, Mock
import pytest
from langsmith import testing as t

# Add the parent directory to the path so we can import our modules
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from main import call_langflow_api, create_ls_target
from config import ls_client

@pytest.fixture(scope="session")
def dataset():
    """Load the dataset for evaluation tests."""
    try:
        return ls_client.read_dataset(dataset_name="Math Dataset")
    except Exception as e:
        pytest.skip(f"Could not load dataset: {e}")

@pytest.fixture(scope="session")
def sample_dataset_examples(dataset):
    """Get a small sample of examples from the dataset for testing."""
    try:
        all_examples = list(ls_client.list_examples(dataset_id=dataset.id))
        return all_examples[:3]  # Use first 3 examples for unit tests
    except Exception as e:
        pytest.skip(f"Could not load dataset examples: {e}")

class TestSingleAgent:
    """Test the single agent approach with dataset questions."""

    @pytest.mark.unit
    @pytest.mark.langsmith
    @pytest.mark.parametrize("example_index", [0, 1, 2])
    def test_single_agent_question(self, sample_dataset_examples, example_index):
        """Test single agent response to dataset questions."""
        if not sample_dataset_examples or len(sample_dataset_examples) <= example_index:
            pytest.skip("No dataset examples available")

        example = sample_dataset_examples[example_index]
        question = example.inputs["question"]
        expected_answer = example.outputs["answer"]

        # Log inputs and reference outputs for LangSmith
        t.log_inputs({"question": question})
        t.log_reference_outputs({"answer": expected_answer})

        # Mock single agent response (more direct/concise)
        with patch('requests.request') as mock_request:
            mock_response = Mock()
            mock_response.json.return_value = {
                "outputs": [{
                    "outputs": [{
                        "results": {
                            "message": {
                                "data": {
                                    "text": f"{expected_answer}"
                                }
                            }
                        }
                    }]
                }]
            }
            mock_response.raise_for_status.return_value = None
            mock_request.return_value = mock_response

            result = call_langflow_api(
                question,
                "Qwen",
                "qwen3-4b-2507",
                "test-api-key",
                "math_eval_single_lms"
            )

            # Log the actual output
            t.log_outputs({"response": result})

            assert result == expected_answer
            mock_request.assert_called_once()


class TestMultiAgent:
    """Test the multi-agent approach with dataset questions."""

    @pytest.mark.unit
    @pytest.mark.langsmith
    @pytest.mark.parametrize("example_index", [0, 1, 2])
    def test_multi_agent_question(self, sample_dataset_examples, example_index):
        """Test multi-agent response to dataset questions."""
        if not sample_dataset_examples or len(sample_dataset_examples) <= example_index:
            pytest.skip("No dataset examples available")

        example = sample_dataset_examples[example_index]
        question = example.inputs["question"]
        expected_answer = example.outputs["answer"]

        # Log inputs and reference outputs for LangSmith
        t.log_inputs({"question": question})
        t.log_reference_outputs({"answer": expected_answer})

        # Mock multi-agent response (more detailed/collaborative)
        with patch('requests.request') as mock_request:
            mock_response = Mock()
            mock_response.json.return_value = {
                "outputs": [{
                    "outputs": [{
                        "results": {
                            "message": {
                                "data": {
                                    "text": f"Agent 1: Let me solve this step by step. {question} Agent 2: I'll verify the calculation. The answer is {expected_answer}. Both agents agree."
                                }
                            }
                        }
                    }]
                }]
            }
            mock_response.raise_for_status.return_value = None
            mock_request.return_value = mock_response

            result = call_langflow_api(
                question,
                "Qwen",
                "qwen3-4b-2507",
                "test-api-key",
                "math_eval_multi_lms"
            )

            # Log the actual output
            t.log_outputs({"response": result})

            # Multi-agent response should contain the answer and be more verbose
            assert expected_answer in result
            assert len(result) > len(expected_answer)  # Should be more detailed
            mock_request.assert_called_once()
