"""Leave me alone linter """
import os
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
