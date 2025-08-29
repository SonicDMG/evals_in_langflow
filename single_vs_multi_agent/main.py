"""
This script runs single vs multi agent evaluations
and compares their performance using LangSmith.
"""
import uuid
import logging
import requests
from rich.logging import RichHandler
from rich.console import Console
from config import (
    ls_client, # LangSmith client
    langflow_api_key, # LangFlow API key
    log, # Rich-formatted logger
    MODELS_TO_TEST, # List of models to test
)
from langsmith import traceable

# Create a minimal app logger for clean output
app_log = logging.getLogger("app")
app_log.setLevel(logging.DEBUG)

# Create a minimal RichHandler that shows only the message
minimal_handler = RichHandler(
    level=logging.DEBUG,
    console=Console(stderr=True),
    markup=False,
    log_time_format="",  # Empty string instead of None to prevent strftime error
    show_path=False,
    show_level=False,
    rich_tracebacks=False,
)
app_log.addHandler(minimal_handler)

# Prevent propagation to parent logger to avoid duplicate output
app_log.propagate = False

# Load the Math Dataset for evaluation
dataset = ls_client.read_dataset(dataset_name="Math Dataset")

# Configuration for single vs multi agent comparison
AGENT_ID = "Agent-AQzDw"
ENDPOINT_NAMES = ["math_eval_single_lms", "math_eval_multi_lms"]

@traceable(name="langflow_agent_run_api", client=ls_client)
def call_langflow_api(input_value, provider, model_name, api_key, endpoint_name):
    """
    Call the Langflow API to run the specified endpoint.
    """
    app_log.debug("call_langflow_api input_value: %s", input_value)
    
    # API Configuration
    url = f"http://localhost:7860/api/v1/run/{endpoint_name}"

    # Request payload configuration
    payload = {
        "output_type": "chat",
        "input_type": "chat",
        "input_value": input_value,
        "session_id": str(uuid.uuid4()),
        "tweaks": {
            AGENT_ID: {
                "agent_llm": provider,
                "model_name": model_name,
                "api_key": api_key
            }
        }
    }

    # Request headers
    headers = {
        "Content-Type": "application/json",
        "x-api-key": langflow_api_key
    }

    try:
        # Send API request
        result = requests.request("POST", url, json=payload, headers=headers, timeout=300)
        result.raise_for_status()

        response_json = result.json()
        output = (
            response_json.get("outputs")[0]
            .get("outputs")[0]
            .get("results")
            .get("message")
            .get("data")
            .get("text")
        )
        app_log.debug("call_langflow_api output: %s", output)
        return output

    except requests.exceptions.RequestException as e:
        log.error("Error making API request: %s", e)
        return None
    except (ValueError, TypeError) as e:
        log.error("Error parsing response: %s", e)
        return None


def create_ls_target(provider, model_name, api_key, endpoint_name):
    """
    Create a LangSmith target function for the Langflow API.
    """
    def ls_target(inputs: dict) -> dict:
        app_log.debug("ls_target received inputs: %s", inputs)
        
        # Extract the question from the nested structure
        question = inputs.get("question")
        if question is None and "inputs" in inputs:
            question = inputs["inputs"].get("question")
        
        # Extract metadata if available (for math problems with units/rounding)
        metadata = inputs.get("metadata", {})
        if not metadata and "metadata" in inputs:
            metadata = inputs["metadata"]
        
        # Enhance the question with metadata context if available
        enhanced_question = question
        if metadata:
            unit = metadata.get("Unit")
            rounding = metadata.get("Rounding")

            if unit or rounding:
                context_parts = []
                if unit:
                    context_parts.append(f"Use units: {unit}")
                if rounding:
                    context_parts.append(f"Rounding: {rounding}")

                if context_parts:
                    enhanced_question = f"{question}\n\nContext: {' | '.join(context_parts)}"
                    app_log.debug("Enhanced question with metadata: %s", enhanced_question)

        return {"response": call_langflow_api(enhanced_question, provider, model_name, api_key, endpoint_name)}
    
    return ls_target


def run_evaluation_for_endpoint(endpoint_name):
    """
    Run evaluation for a specific endpoint (single or multi agent).
    """
    log.info("Running evaluation for %s", endpoint_name)
    
    for model_config in MODELS_TO_TEST:
        PROVIDER = model_config["provider"]
        MODEL_NAME = model_config["model_name"]
        if "api_key" in model_config:
            API_KEY = model_config["api_key"]
        else:
            API_KEY = None

        target_func = create_ls_target(PROVIDER, MODEL_NAME, API_KEY, endpoint_name)

        log.info(
            "Running evaluation for [bold blue]%s[/bold blue] - [bold green]%s[/bold green] - %s",
            PROVIDER,
            MODEL_NAME,
            API_KEY,
        )
        
        experiment_results = ls_client.evaluate(
            target_func,
            data=dataset.name,
            metadata={
                "llm.provider": PROVIDER,
                "llm.model": MODEL_NAME,
                "endpoint.type": endpoint_name,
            },
            experiment_prefix=f"{endpoint_name}-{PROVIDER}-{MODEL_NAME}"
        )
        
        log.info("Completed evaluation for %s - %s - %s", PROVIDER, MODEL_NAME, endpoint_name)


if __name__ == "__main__":
    log.info("\n[bold]Starting Single vs Multi Agent Evaluation...[/bold]")
    
    # Run evaluations for both single and multi agent endpoints
    for endpoint_name in ENDPOINT_NAMES:
        run_evaluation_for_endpoint(endpoint_name)
    
    log.info("\n[bold]Single vs Multi Agent Evaluation Complete![/bold]")

