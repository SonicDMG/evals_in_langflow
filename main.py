"""
This script runs a Langflow agent flow
and evaluates its performance using LangSmith.
"""
import uuid
import requests
from langsmith import traceable
from config import (
    ls_client, # LangSmith client
    langflow_api_key # LangFlow API key
)
from dataset import dataset # LangSmith dataset
from judge import ( # LLM-as-judge evaluators
    helpfulness, # helpfulness evaluator
    concision # concision evaluator
)

PROVIDER = "Google Generative AI"
MODEL_NAME = "gemini-2.5-flash"
AGENT_ID = "Agent-20ggR"
ENDPOINT_NAME = "evals_in_langflow"

# ===========================
# Run the eval
# ===========================
@traceable(name="langflow_agent_run_api")
def call_langflow_api(input_value):
    """
    Call the Langflow API to run the evals_in_langflow flow.
    """
    print(f"[DEBUG] call_langflow_api input_value: {input_value}")  # Debug input
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
                "agent_llm": PROVIDER,
                "model_name": MODEL_NAME
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
        result = requests.request("POST", url, json=payload, headers=headers, timeout=30)
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
        print(f"[DEBUG] call_langflow_api output: {output}")  # Debug output
        return output

    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
    except ValueError as e:
        print(f"Error parsing response: {e}")


def ls_target(inputs: dict) -> dict:
    print(f"[DEBUG] ls_target received inputs: {inputs}")
    # Extract the question from the nested structure
    question = inputs.get("question")
    if question is None and "inputs" in inputs:
        question = inputs["inputs"].get("question")
    return {"response": call_langflow_api(question)}


if __name__ == "__main__":
    experiment_results = ls_client.evaluate(
        ls_target, # your target function
        data=dataset.name, # dataset name or ID
        evaluators=[concision, helpfulness], # list of evaluator funcs
        experiment_prefix=f"{ENDPOINT_NAME}-{PROVIDER}-{MODEL_NAME}" # experiment name in LangSmith
    )

    print("▶ Evaluation URL:", experiment_results)
