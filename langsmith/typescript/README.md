# LangSmith TypeScript Evaluation

This directory contains the TypeScript script for running evaluations of a Langflow agent using LangSmith.

## Setup

1.  **Environment Variables**: This project uses a single `.env` file located in the root of the `evals_in_langflow` repository. Make sure it is populated with the necessary API keys and configuration. The script will automatically load these variables.

    ```bash
    # .env file in the root directory
    LANGCHAIN_API_KEY="your-langsmith-api-key"
    LANGCHAIN_PROJECT="your-langsmith-project-name"
    OPENAI_API_KEY="your-openai-api-key"
    LANGFLOW_API_KEY="your-langflow-api-key"
    LANGFLOW_URL="http://127.0.0.1:7860" # Optional: defaults to localhost
    ```

2.  **Install Dependencies**: Navigate to this directory and install the required Node.js packages using npm.

    ```bash
    cd langsmith/typescript
    npm install
    ```

## Running the Evaluation

To run the evaluation, execute the `index.ts` script from this directory using `ts-node`:

```bash
npm run start
```

The script will iterate through the models defined in `MODELS_TO_TEST`, run the agent against the dataset for each, and record the results in your LangSmith project. 