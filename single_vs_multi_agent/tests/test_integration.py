"""
Integration tests for single vs multi agent evaluations.
These tests make real API calls to Langflow and use actual external dependencies.
"""
import sys
from pathlib import Path
import pytest
from langsmith import testing as t

# Add the parent directory to the path so we can import our modules
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from main import call_langflow_api, create_ls_target
from config import ls_client, langflow_api_key

# Skip all tests if Langflow API key is not available
pytestmark = pytest.mark.skipif(
    not langflow_api_key,
    reason="LANGFLOW_API_KEY not set - skipping integration tests"
)

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
        # Return first 3 examples for faster test execution
        return all_examples[:3]
    except Exception as e:
        pytest.skip(f"Could not load dataset examples: {e}")

class TestSingleAgentIntegration:
    """Test the single agent approach with real API calls."""
    
    @pytest.mark.integration
    @pytest.mark.real_api
    @pytest.mark.langsmith
    @pytest.mark.parametrize("example_index", [0, 1, 2])
    def test_single_agent_real_question(self, sample_dataset_examples, example_index):
        """Test single agent with real Langflow API call using dataset questions."""
        if not sample_dataset_examples or len(sample_dataset_examples) <= example_index:
            pytest.skip("No dataset examples available")
        
        example = sample_dataset_examples[example_index]
        question = example.inputs["question"]
        expected_answer = example.outputs["answer"]
        
        # Log inputs and reference outputs for LangSmith
        t.log_inputs({"question": question})
        t.log_reference_outputs({"answer": expected_answer})
        
        # Make real API call to Langflow single agent endpoint
        response = call_langflow_api(
            question,
            "Qwen",
            "qwen3-4b-2507", 
            None,
            "math_eval_single_lms"
        )
        
        # Log the actual output
        t.log_outputs({"response": response})
        
        # Basic assertions
        assert response is not None, "Should receive a response from real API"
        assert len(response) > 0, "Response should not be empty"

class TestMultiAgentIntegration:
    """Test the multi-agent approach with real API calls."""
    
    @pytest.mark.integration
    @pytest.mark.real_api
    @pytest.mark.langsmith
    @pytest.mark.parametrize("example_index", [0, 1, 2])
    def test_multi_agent_real_question(self, sample_dataset_examples, example_index):
        """Test multi-agent with real Langflow API call using dataset questions."""
        if not sample_dataset_examples or len(sample_dataset_examples) <= example_index:
            pytest.skip("No dataset examples available")
        
        example = sample_dataset_examples[example_index]
        question = example.inputs["question"]
        expected_answer = example.outputs["answer"]
        
        # Log inputs and reference outputs for LangSmith
        t.log_inputs({"question": question})
        t.log_reference_outputs({"answer": expected_answer})
        
        # Make real API call to Langflow multi-agent endpoint
        response = call_langflow_api(
            question,
            "Qwen",
            "qwen3-4b-2507", 
            None,
            "math_eval_multi_lms"
        )
        
        # Log the actual output
        t.log_outputs({"response": response})
        
        # Basic assertions
        assert response is not None, "Should receive a response from real API"
        assert len(response) > 0, "Response should not be empty"