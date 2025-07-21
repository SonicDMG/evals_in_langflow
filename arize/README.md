# Arize Phoenix Evaluations

This directory contains scripts and configurations for running LLM evaluations on a Langflow agent using the [Arize Phoenix](https://www.arize.com/phoenix/) platform. The script runs a set of questions from a predefined dataset through a Langflow agent and uses Phoenix to log the results, including evaluation metrics and token/cost data.

## Prerequisites

*   Python 3.8+
*   A running instance of [Langflow](https://langflow.dev/) with an agent flow accessible via its API.
*   An active Arize account with access to Phoenix.

## Setup

1.  **Configure Environment Variables**

    Create a `.env` file in the root of this project (the `evals_in_langflow` directory). This file will store the necessary API keys and endpoints. Populate it with the following variables:

    ```bash
    # Langflow API Key
    LANGFLOW_API_KEY="your_langflow_api_key"

    # Arize Phoenix Cloud Credentials
    PHOENIX_API_KEY="your_phoenix_api_key"
    OTEL_EXPORTER_OTLP_HEADERS="X-API-KEY=your_phoenix_api_key"
    PHOENIX_COLLECTOR_ENDPOINT="https://app.phoenix.arize.com"

    # OpenAI API Key (or other provider keys)
    OPENAI_API_KEY="your_openai_api_key"
    ```

2.  **Create a Virtual Environment**

    It is highly recommended to use a virtual environment to manage dependencies.

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install Dependencies**

    Install the required Python packages using the `requirements.txt` file.

    ```bash
    pip install -r arize/requirements.txt
    ```

## Running the Evaluations

Once the setup is complete, you can run the evaluation script from the root of the `evals_in_langflow` directory:

```bash
python arize/main.py
```

The script will print the progress and provide a link to the experiment results in the Phoenix UI.

## How It Works

*   `main.py`: The main script that orchestrates the evaluation process. It initializes the Phoenix tracer, loads the dataset, runs the experiment by calling the Langflow API for each example, and logs the results.
*   `dataset.py`: Defines the dataset of questions and answers used for the evaluation.
*   `judge.py`: Contains the evaluator functions (e.g., `helpfulness`, `concision`) that are used by Phoenix to score the LLM's responses.
*   `config.py`: Loads environment variables, configures the logger, and defines the list of LLM models to be tested. 