"""
This file contains the configuration for the LangSmith Python client.
"""
import os
import logging
from rich.logging import RichHandler
from rich.console import Console
from dotenv import load_dotenv
from openai import OpenAI
import phoenix as px

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variables
phoenix_endpoint = os.getenv("PHOENIX_COLLECTOR_ENDPOINT")
phoenix_api_key = os.getenv("PHOENIX_API_KEY")
otel_exporter_otlp_headers = os.getenv("OTEL_EXPORTER_OTLP_HEADERS")
phoenix_client_headers = os.getenv("PHOENIX_CLIENT_HEADERS")
openai_api_key = os.getenv("OPENAI_API_KEY")
langflow_api_key = os.getenv("LANGFLOW_API_KEY")

# initialize clients
phoenix_client = px.Client(
    endpoint=phoenix_endpoint,
    api_key=phoenix_api_key,
)
openai_client = OpenAI(api_key=openai_api_key)

# A list of models to test. You can add more models here.
# The `provider` should match the provider name in Langflow.
# The `model_name` should match the model name for that provider.
# The `api_key` should match your global variable for that provider in Langflow.
MODELS_TO_TEST = [
    {
        "provider": "Google Generative AI",
        "model_name": "gemini-2.5-flash",
        "api_key": "google_ai__API_KEY"
    },
    {
        "provider": "OpenAI",
        "model_name": "gpt-4.1-mini",
        "api_key": "openai__API_KEY"
    },
    {
        "provider": "OpenAI",
        "model_name": "gpt-4.0-mini",
        "api_key": "openai__API_KEY"
    },
    {
        "provider": "OpenAI",
        "model_name": "gpt-4.1-nano",
        "api_key": "openai__API_KEY"
    },
    #{
    #    "provider": "Anthropic",
    #    "model_name": "claude-3-5-sonnet-latest",
    #    "api_key": "anthropic__API_KEY"
    #}
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
