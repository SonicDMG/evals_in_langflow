"""
This script creates or fetches an eval dataset using LangSmithfor the Langflow agent.
"""
from config import ls_client # LangSmith client

# Dataset name and description as they appear in LangSmith
DATASET_NAME = "langflow-agent-evals"
DATASET_DESC = "QA checks for our Langflow agent"

# Define the examples ONCE
examples = [
    {
        "inputs": {"question": "How do you define a function in Python?"},
        "outputs": {
            "answer": (
                "In Python, you define a function using the 'def' keyword "
                "followed by the function name,"
                "parameters in parentheses, and a colon. The function body is indented below."
            )
        },
    },
    {
        "inputs": {"question": "What is the difference between a list and a tuple in Python?"},
        "outputs": {
            "answer": (
                "Lists are mutable (can be changed after creation) while tuples are immutable "
                "(cannot be changed after creation)."
                "Lists use square brackets [] and tuples use parentheses ()."
            )
        },
    },
    {
        "inputs": {"question": "What does the 'self' parameter in Python class methods represent?"},
        "outputs": {
            "answer": (
                "The 'self' parameter in Python class methods refers to the instance of the class."
                "It allows access to the attributes and methods of the class."
            )
        },
    },
    {
        "inputs": {"question": "What is a lambda function in Python?"},
        "outputs": {
            "answer": (
                "A lambda function is an anonymous function defined using the 'lambda' keyword."
                "It can take any number of arguments but can only have one expression."
            )
        },
    }
]

datasets = ls_client.list_datasets()
print("Datasets found:", [d.name for d in datasets])
print("Has dataset?", ls_client.has_dataset(dataset_name=DATASET_NAME))

if ls_client.has_dataset(dataset_name=DATASET_NAME):
    dataset = ls_client.read_dataset(dataset_name=DATASET_NAME)
    # Check if dataset is empty
    examples_list = list(ls_client.list_examples(dataset_id=dataset.id))
    print("Examples returned by list_examples:", examples_list)
    print("Number of examples:", len(examples_list))
    if not examples_list:
        print("Dataset is empty, populating examples...")
        for ex in examples:
            ls_client.create_example(inputs=ex["inputs"], outputs=ex["outputs"], dataset_id=dataset.id)
    else:
        print("Dataset exists and is not empty. No action needed.")
else:
    print("Dataset does not exist. Creating and populating examples...")
    dataset = ls_client.create_dataset(
        dataset_name=DATASET_NAME,
        description=DATASET_DESC
    )
    for ex in examples:
        ls_client.create_example(inputs=ex["inputs"], outputs=ex["outputs"], dataset_id=dataset.id)
