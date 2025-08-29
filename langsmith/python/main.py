"""
This script runs a Langflow agent flow
and evaluates its performance using LangSmith.
"""
import uuid
import requests
from config import (
    ls_client, # LangSmith client
    langflow_api_key, # LangFlow API key
    log, # Rich-formatted logger
    MODELS_TO_TEST, # List of models to test
)
from dataset import dataset # LangSmith dataset
from judge import ( # LLM-as-judge evaluators
    helpfulness, # helpfulness evaluator
    concision # concision evaluator
)
from langsmith import traceable

AGENT_ID = "Agent-AQzDw"
ENDPOINT_NAME = "evals_in_langflow"

# ===========================
# Run the eval
# ===========================
@traceable(name="langflow_agent_run_api", client=ls_client)
def call_langflow_api(input_value, provider, model_name, api_key):
    """
    Call the Langflow API to run the evals_in_langflow flow.
    """
    log.debug("call_langflow_api input_value: %s", input_value)  # Debug input
    # API Configuration
    url = f"http://127.0.0.1:7860/api/v1/run/{ENDPOINT_NAME}"

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
        "x-api-key": langflow_api_key  # Authentication key from environment variable
    }

    try:
        # Send API request
        result = requests.request("POST", url, json=payload, headers=headers, timeout=300)
        result.raise_for_status()  # Raise exception for bad status codes

        response_json = result.json()
        output = (
            response_json.get("outputs")[0]
            .get("outputs")[0]
            .get("results")
            .get("message")
            .get("data")
            .get("text")
        )
        log.debug("call_langflow_api output: %s", output)  # Debug output
        return output

    except requests.exceptions.RequestException as e:
        log.error("Error making API request: %s", e)
    except ValueError as e:
        log.error("Error parsing response: %s", e)


def create_ls_target(provider, model_name, api_key):
    """
    Create a LangSmith target function for the Langflow API.
    """
    def ls_target(inputs: dict) -> dict:
        log.debug("ls_target received inputs: %s", inputs)
        # Extract the question from the nested structure
        question = inputs.get("question")
        if question is None and "inputs" in inputs:
            question = inputs["inputs"].get("question")
        return {"response": call_langflow_api(question, provider, model_name, api_key)}
    return ls_target


if __name__ == "__main__":
    log.info("\n[bold]Starting LangSmith Evals...[/bold]")
    for model_config in MODELS_TO_TEST:
        PROVIDER = model_config["provider"]
        MODEL_NAME = model_config["model_name"]
        API_KEY = model_config["api_key"]

        target_func = create_ls_target(PROVIDER, MODEL_NAME, API_KEY)

        log.info(
            "Running evaluation for [bold blue]%s[/bold blue] - [bold green]%s[/bold green] - %s",
            PROVIDER,
            MODEL_NAME,
            API_KEY,
        )
        experiment_results = ls_client.evaluate(
            target_func,  # your target function
            data=dataset.name,  # dataset name or ID
            evaluators=[concision, helpfulness],  # list of evaluator funcs
            metadata={
                "llm.provider": PROVIDER,
                "llm.model": MODEL_NAME,
            },
            experiment_prefix=f"{ENDPOINT_NAME}-{PROVIDER}-{MODEL_NAME}"  # experiment name in LangSmith
        )
