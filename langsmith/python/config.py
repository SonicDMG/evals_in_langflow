"""Leave me alone linter """
import os
import logging
from rich.logging import RichHandler
from rich.console import Console
from dotenv import load_dotenv
from langsmith import Client as LSClient, wrappers
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variable
langchain_api_key = os.getenv("LANGCHAIN_API_KEY")
langchain_project = os.getenv("LANGCHAIN_PROJECT")
openai_api_key = os.getenv("OPENAI_API_KEY")
langflow_api_key = os.getenv("LANGFLOW_API_KEY")

# initialize clients
ls_client = LSClient()
openai_client = wrappers.wrap_openai(OpenAI(api_key=openai_api_key))

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
