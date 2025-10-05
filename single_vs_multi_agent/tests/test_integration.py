"""
Integration tests for single vs multi agent evaluations.
These tests make real API calls to Langflow and use actual external dependencies.
"""
import pytest
from langsmith import testing as t
from ..config import (
    ls_client,
    langflow_api_key,
    CORRECTNESS_EVALUATOR,
    CONCISENESS_EVALUATOR,
    MODELS_TO_TEST,
    #HALLUCINATION_EVALUATOR
)
from ..main import call_langflow_api

# Skip all tests if Langflow API key is not available
pytestmark = pytest.mark.skipif(
    not langflow_api_key,
    reason="LANGFLOW_API_KEY not set - skipping integration tests"
)

DATASET_NAME = "Math Dataset"

@pytest.fixture(scope="session")
def dataset():
    """Load the dataset for evaluation tests."""
    try:
        return ls_client.read_dataset(dataset_name=DATASET_NAME)
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

@pytest.mark.integration
@pytest.mark.real_api
@pytest.mark.langsmith
@pytest.mark.parametrize("model_config", MODELS_TO_TEST)
@pytest.mark.parametrize("example_index", [0, 1, 2])
def test_single_agent_real_question(sample_dataset_examples, model_config, example_index):
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
        model_config["provider"],
        model_config["model_name"],
        model_config.get("api_key"),
        "math_eval_single_lms"
    )

    # Log the actual output
    t.log_outputs({"response": response})

    # Apply correctness evaluator
    if CORRECTNESS_EVALUATOR:
        try:
            CORRECTNESS_EVALUATOR(
                inputs=question,
                outputs=response,
                reference_outputs=expected_answer
            )
        except Exception as e:
            print(f"Correctness evaluator error: {e}")

    # Apply conciseness evaluator
    if CONCISENESS_EVALUATOR:
        try:
            CONCISENESS_EVALUATOR(
                inputs=question,
                outputs=response,
                reference_outputs=expected_answer
            )
        except Exception as e:
            print(f"Conciseness evaluator error: {e}")

    # Basic assertions
    assert response is not None, "Should receive a response from real API"
    assert len(response) > 0, "Response should not be empty"

@pytest.mark.integration
@pytest.mark.real_api
@pytest.mark.langsmith
@pytest.mark.parametrize("model_config", MODELS_TO_TEST)
@pytest.mark.parametrize("example_index", [0, 1, 2])
def test_multi_agent_real_question(sample_dataset_examples, model_config, example_index):
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
        model_config["provider"],
        model_config["model_name"],
        model_config.get("api_key"),
        "math_eval_multi_lms"
    )

    # Log the actual output
    t.log_outputs({"response": response})

    # Apply correctness evaluator
    if CORRECTNESS_EVALUATOR:
        try:
            CORRECTNESS_EVALUATOR(
                inputs=question,
                outputs=response,
                reference_outputs=expected_answer
            )
        except Exception as e:
            print(f"Correctness evaluator error: {e}")

    # Apply conciseness evaluator
    if CONCISENESS_EVALUATOR:
        try:
            CONCISENESS_EVALUATOR(
                inputs=question,
                outputs=response,
                reference_outputs=expected_answer
            )
        except Exception as e:
            print(f"Conciseness evaluator error: {e}")

    # Basic assertions
    assert response is not None, "Should receive a response from real API"
    assert len(response) > 0, "Response should not be empty"

@pytest.mark.integration
@pytest.mark.real_api
@pytest.mark.langsmith
@pytest.mark.parametrize("model_config", MODELS_TO_TEST)
@pytest.mark.parametrize("example_index", [0, 1, 2])
def test_noexp_agent_real_question(sample_dataset_examples, model_config, example_index):
    """Test no explanation agent with real Langflow API call using dataset questions."""
    if not sample_dataset_examples or len(sample_dataset_examples) <= example_index:
        pytest.skip("No dataset examples available")

    example = sample_dataset_examples[example_index]
    question = example.inputs["question"]
    expected_answer = example.outputs["answer"]

    # Log inputs and reference outputs for LangSmith
    t.log_inputs({"question": question})
    t.log_reference_outputs({"answer": expected_answer})

    # Make real API call to Langflow no explanation endpoint
    response = call_langflow_api(
        question,
        model_config["provider"],
        model_config["model_name"],
        model_config.get("api_key"),
        "math_eval_noexp_lms"
    )

    # Log the actual output
    t.log_outputs({"response": response})

    # Apply correctness evaluator
    if CORRECTNESS_EVALUATOR:
        try:
            CORRECTNESS_EVALUATOR(
                inputs=question,
                outputs=response,
                reference_outputs=expected_answer
            )
        except Exception as e:
            print(f"Correctness evaluator error: {e}")

    # Apply conciseness evaluator
    if CONCISENESS_EVALUATOR:
        try:
            CONCISENESS_EVALUATOR(
                inputs=question,
                outputs=response,
                reference_outputs=expected_answer
            )
        except Exception as e:
            print(f"Conciseness evaluator error: {e}")

    # Basic assertions
    assert response is not None, "Should receive a response from real API"
    assert len(response) > 0, "Response should not be empty"
