"""
This file contains the configuration for the Single vs Multi Agent evaluation.
"""
import os
import logging
from rich.logging import RichHandler
from rich.console import Console
from dotenv import load_dotenv
from openevals.llm import create_llm_as_judge
from openevals.prompts import (
    CORRECTNESS_PROMPT,
    CONCISENESS_PROMPT,
    HALLUCINATION_PROMPT
)
from langsmith import Client as LSClient

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variables
langchain_api_key = os.getenv("LANGCHAIN_API_KEY")
langchain_project = os.getenv("LANGCHAIN_PROJECT")
langflow_api_key = os.getenv("LANGFLOW_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

# initialize clients
ls_client = LSClient(auto_batch_tracing=True)

# Initialize evaluators
if openai_api_key:

    # Create the evaluators
    CORRECTNESS_EVALUATOR = create_llm_as_judge(
        prompt=CORRECTNESS_PROMPT,
        feedback_key="correctness",
        model="openai:gpt-5-mini",
    )

    CONCISENESS_EVALUATOR = create_llm_as_judge(
        prompt=CONCISENESS_PROMPT,
        feedback_key="conciseness",
        model="openai:gpt-5-mini",
    )

    HALLUCINATION_EVALUATOR = create_llm_as_judge(
        prompt=HALLUCINATION_PROMPT,
        feedback_key="hallucination",
        model="openai:gpt-5-mini",
    )
else:
    # If no OpenAI key, set evaluators to None
    CORRECTNESS_EVALUATOR = None
    CONCISENESS_EVALUATOR = None
    HALLUCINATION_EVALUATOR = None

# A list of models to test for single vs multi agent comparison
# The `provider` should match the provider name in Langflow.
# The `model_name` should match the model name for that provider.
# The `api_key` should match the global variable for that provider in Langflow.
MODELS_TO_TEST = [
    #{
    #    "provider": "Google Generative AI",
    #    "model_name": "gemini-2.5-flash",
    #    "api_key": "google_ai__API_KEY"
    #},
    #{
    #    "provider": "OpenAI",
    #    "model_name": "gpt-4.1",
    #    "api_key": "openai__API_KEY"
    #},
    #{
    #    "provider": "OpenAI",
    #    "model_name": "gpt-4.1-mini",
    #    "api_key": "openai__API_KEY"
    #},
    #{
    #    "provider": "OpenAI",
    #    "model_name": "gpt-4.1-nano",
    #    "api_key": "openai__API_KEY"
    #},
    #{
    #    "provider": "OpenAI",
    #    "model_name": "gpt-oss-20b"
    #},
    #{
    #    "provider": "MistralAI",
    #    "model_name": "mathstral-7b-v0.1"
    #},
    {
        "provider": "Qwen",
        "model_name": "qwen3-4b-2507",
        "api_key": None
    },
    #{
    #    "provider": "Anthropic",
    #    "model_name": "claude-3-7-sonnet-latest",
    #    "api_key": "anthropic__API_KEY"
    #}
]

# ==============================================================================
# LOGGING
# ==============================================================================
# CONFIGURE THE LOGGER
log = logging.getLogger("rich")
log.setLevel(logging.DEBUG)  # Set the lowest level for the logger

# CREATE A RICH HANDLER FOR CONSOLE OUTPUT (DEBUG and above)
console_handler = RichHandler(
    level=logging.DEBUG,
    console=Console(stderr=True),
    markup=True,
    log_time_format="%Y-%m-%d %H:%M:%S",
    show_path=False,
)

# CREATE A FILE HANDLER FOR DETAILED DEBUG LOGS
file_handler = logging.FileHandler("single_vs_multi_agent_eval.log")
file_handler.setLevel(logging.DEBUG)

# CREATE A FORMATTER FOR THE FILE HANDLER
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# ADD THE HANDLERS TO THE LOGGER
log.addHandler(console_handler)
log.addHandler(file_handler)
# ==============================================================================
