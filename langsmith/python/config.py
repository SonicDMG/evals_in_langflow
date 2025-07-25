"""
This file contains the configuration for the LangSmith Python client.
"""
import os
import logging
from rich.logging import RichHandler
from rich.console import Console
from dotenv import load_dotenv
from openai import OpenAI
from langsmith import Client as LSClient, wrappers

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variables
langchain_api_key = os.getenv("LANGCHAIN_API_KEY")
langchain_project = os.getenv("LANGCHAIN_PROJECT")
openai_api_key = os.getenv("OPENAI_API_KEY")
langflow_api_key = os.getenv("LANGFLOW_API_KEY")

# initialize clients
ls_client = LSClient(auto_batch_tracing=True)
openai_client = wrappers.wrap_openai(OpenAI(api_key=openai_api_key))

# A list of models to test. You can add more models here.
# The `provider` should match the provider name in Langflow.
# The `model_name` should match the model name for that provider.
# The `api_key` should match the global variable for that provider in Langflow.
MODELS_TO_TEST = [
    #{
    #    "provider": "Google Generative AI",
    #    "model_name": "gemini-2.5-flash",
    #    "api_key": "google_ai__API_KEY"
    #},
    {
        "provider": "OpenAI",
        "model_name": "gpt-4.1",
        "api_key": "openai__API_KEY"
    },
    {
        "provider": "OpenAI",
        "model_name": "gpt-4.1-mini",
        "api_key": "openai__API_KEY"
    },
    {
        "provider": "OpenAI",
        "model_name": "gpt-4.1-nano",
        "api_key": "openai__API_KEY"
    },
    {
        "provider": "Anthropic",
        "model_name": "claude-3-7-sonnet-latest",
        "api_key": "anthropic__API_KEY"
    }
]

# ==============================================================================
# LOGGING
# ==============================================================================
# CONFIGURE THE LOGGER
log = logging.getLogger("rich")
log.setLevel(logging.DEBUG)  # Set the lowest level for the logger

# CREATE A RICH HANDLER FOR CONSOLE OUTPUT (INFO and above)
console_handler = RichHandler(
    level=logging.INFO,
    console=Console(stderr=True),
    markup=True,
    log_time_format="%Y-%m-%d %H:%M:%S",
    show_path=False,
)

# CREATE A FILE HANDLER FOR DETAILED DEBUG LOGS
file_handler = logging.FileHandler("langflow_eval.log")
file_handler.setLevel(logging.DEBUG)

# CREATE A FORMATTER FOR THE FILE HANDLER
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# ADD THE HANDLERS TO THE LOGGER
log.addHandler(console_handler)
log.addHandler(file_handler)
# ==============================================================================
