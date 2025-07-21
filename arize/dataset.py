"""
This script creates or fetches an eval dataset using Arize Pheonix for the Langflow agent.
"""
from config import phoenix_client, log # Arize client
import pandas as pd

# Dataset name and description as they appear in LangSmith
DATASET_NAME = "langflow-agent-evals"
DATASET_DESC = "QA checks for our Langflow agent"

# Define the examples ONCE
examples = pd.DataFrame(
    [
        {
            "question": "How do you define a function in Python?",
            "answer": (
                "In Python, you define a function using the 'def' keyword "
                "followed by the function name,"
                "parameters in parentheses, and a colon. The function body is indented below."
            )
        },
        {
            "question": "What is the difference between a list and a tuple in Python?",
            "answer": (
                "Lists are mutable (can be changed after creation) while tuples are immutable "
                "(cannot be changed after creation)."
                "Lists use square brackets [] and tuples use parentheses ()."
            )
        },
        {
            "question": "What does the 'self' parameter in Python class methods represent?",
            "answer": (
                "The 'self' parameter in Python class methods refers to the instance of the class."
                "It allows access to the attributes and methods of the class."
            )
        },
        {
            "question": "What is a lambda function in Python?",
            "answer": (
                "A lambda function is an anonymous function defined using the 'lambda' keyword."
                "It can take any number of arguments but can only have one expression."
            )
        }
    ]
)

try:
    # Check if the dataset already exists
    dataset = phoenix_client.get_dataset(name=DATASET_NAME)
    log.info("Dataset '%s' already exists. Using existing dataset.", DATASET_NAME)
except ValueError:
    log.info("Dataset '%s' not found. Creating a new dataset...", DATASET_NAME)
    # If the dataset does not exist, upload it
    dataset = phoenix_client.upload_dataset(
        dataframe=examples,
        dataset_name=DATASET_NAME,
        input_keys=["question"],
        output_keys=["answer"],
    )
    log.info("Successfully created dataset '%s'.", DATASET_NAME)
