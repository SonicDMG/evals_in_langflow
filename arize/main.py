"""
This script runs a Langflow agent flow
and evaluates its performance using Arize Phoenix.
"""
import uuid
from functools import partial
import os
import requests
import tiktoken
import nest_asyncio
from phoenix.otel import register
from phoenix.experiments import run_experiment
from opentelemetry import trace
from openinference.semconv.trace import SpanAttributes
from config import (
    log,
    langflow_api_key,
    MODELS_TO_TEST
)
from dataset import dataset
from judge import (
    helpfulness,
    conciseness,
    coherence
)

AGENT_ID = "Agent-20ggR"
ENDPOINT_NAME = "evals_in_langflow"
PROJECT_NAME = "evals_in_langflow"

# Configure the Phoenix tracer
tracer_provider = register(
    protocol="http/protobuf",
    project_name=PROJECT_NAME,
    batch=True,
    #auto_instrument=True
)
tracer = tracer_provider.get_tracer(__name__)

headers = os.getenv("OTEL_EXPORTER_OTLP_HEADERS")
endpoint = os.getenv("PHOENIX_COLLECTOR_ENDPOINT")

@tracer.llm
#@tracer.chain
def call_langflow_api(example, provider, model_name, api_key):
    """
    Call the Langflow API to run the evals_in_langflow flow.
    """
    input_value = example.input["question"]
    log.debug("call_langflow_api input_value: %s", input_value)
    url = f"http://127.0.0.1:7860/api/v1/run/{ENDPOINT_NAME}"
    payload = {
        "output_type": "chat",
        "input_type": "chat",
        "input_value": input_value,
        "session_id": str(uuid.uuid4()),
        "tweaks": {
            AGENT_ID: {
                "agent_llm": provider,
                "model_name": model_name,
                "api_key": api_key,
            }
        },
    }
    headers = {
        "Content-Type": "application/json",
        "x-api-key": langflow_api_key,
    }
    try:
        result = requests.post(url, json=payload, headers=headers, timeout=30)
        result.raise_for_status()
        response_json = result.json()
        output = (
            response_json.get("outputs", [{}])[0]
            .get("outputs", [{}])[0]
            .get("results", {})
            .get("message", {})
            .get("data", {})
            .get("text")
        )

        encoding = tiktoken.get_encoding("cl100k_base")
        prompt_tokens = len(encoding.encode(input_value))
        completion_tokens = len(encoding.encode(output))
        total_tokens = prompt_tokens + completion_tokens

        current_span = trace.get_current_span()
        current_span.set_attributes(
            {
                SpanAttributes.LLM_PROVIDER: provider,
                SpanAttributes.LLM_MODEL_NAME: model_name,
                SpanAttributes.LLM_TOKEN_COUNT_PROMPT: prompt_tokens,
                SpanAttributes.LLM_TOKEN_COUNT_COMPLETION: completion_tokens,
                SpanAttributes.LLM_TOKEN_COUNT_TOTAL: total_tokens,
            }
        )
        log.debug("call_langflow_api output: %s", output)
        return output
    except requests.exceptions.RequestException as e:
        log.error("Error making API request: %s", e)
        return None
    except (ValueError, KeyError, IndexError) as e:
        log.error("Error parsing response: %s", e)
        return None


if __name__ == "__main__":
    nest_asyncio.apply()
    log.info("\n[bold]Starting Arize Phoenix Evals...[/bold]")
    for model_config in MODELS_TO_TEST:
        PROVIDER = model_config["provider"]
        MODEL_NAME = model_config["model_name"]
        API_KEY = model_config["api_key"]

        # Use partial to create a function with the model config
        # because Phoenix expects a task function with only (example) as input.
        # call_langflow_api expects (example, provider, model_name, and api_key)
        task = partial(
            call_langflow_api,
            provider=PROVIDER,
            model_name=MODEL_NAME,
            api_key=API_KEY,
        )

        log.info(
            "Running evaluation for [bold blue]%s[/bold blue] - [bold green]%s[/bold green]",
            PROVIDER,
            MODEL_NAME,
        )
        experiment = run_experiment(
            dataset=dataset,
            task=task,
            evaluators=[helpfulness, conciseness, coherence],
            experiment_name=f"{ENDPOINT_NAME}-{PROVIDER}-{MODEL_NAME}",
        )
        log.info("Experiment results: %s", experiment.url)
