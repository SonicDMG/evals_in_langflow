Evals In
```
██╗      █████╗ ███╗   ██╗ ██████╗  ███████╗██╗      ██████╗  ██╗    ██╗
██║     ██╔══██╗████╗  ██║██╔════╝  ██╔════╝██║     ██╔═══██╗ ██║    ██║
██║     ███████║██╔██╗ ██║██║  ███╗ █████╗  ██║     ██║   ██║ ██║ █╗ ██║
██║     ██╔══██║██║╚██╗██║██║   ██║ ██╔══╝  ██║     ██║   ██║ ██║███╗██║
███████╗██║  ██║██║ ╚████║╚██████╔╝ ██║     ███████╗╚██████╔╝ ╚███╔███╔╝
╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝  ╚═╝     ╚══════╝ ╚═════╝  ╚══╝╚══╝
```

# evals_in_langflow

![GitHub license](https://img.shields.io/github/license/SonicDMG/evals_in_langflow)
![GitHub issues](https://img.shields.io/github/issues/SonicDMG/evals_in_langflow)
![GitHub forks](https://img.shields.io/github/forks/SonicDMG/evals_in_langflow)
![GitHub stars](https://img.shields.io/github/stars/SonicDMG/evals_in_langflow)

[Langflow](https://langflow.org/) agent evaluation framework with integrations for multiple evaluation providers.

## 🌟 Overview

`evals_in_langflow` is a framework for evaluating [Langflow](https://langflow.org/) agents using providers like [LangSmith](https://www.langchain.com/langsmith) and [Arize](https://arize.com/). It provides a structured way to run, judge, and analyze agent outputs against datasets, making it easier to benchmark and improve your Langflow-based LLM applications.

## ✨ Features
- Run agent evaluations against datasets
- Integrate with multiple evaluation providers like [LangSmith](https://www.langchain.com/langsmith) and [Arize](https://arize.com/) for tracing and analytics
- Compare single-agent vs multi-agent performance configurations
- Configurable via environment variables
- Supports both Python and TypeScript ignores for clean development

## Resources
[Using LangSmith with Pytest](https://docs.langchain.com/langsmith/pytest#how-to-run-evaluations-with-pytest-beta)

[Creating code evals in code using LangSmith](https://youtu.be/uqykG9Z8riU?si=nlbW52aSHCcMpocb)

[AI Observability Explained](https://youtu.be/TDcT9ao47Tk?si=5imwX2M4BT8__983)


## 📦 Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/SonicDMG/evals_in_langflow.git
    cd evals_in_langflow
    ```

2.  **Configure environment variables:**
    - Copy `.env.example` to `.env` and fill in your API keys and project info.
    ```bash
    cp .env.example .env
    # Edit .env with your preferred editor
    ```

3.  **Install dependencies:**
    Please refer to the `README.md` file within each provider's subdirectory for detailed installation instructions (e.g., `langsmith/python/README.md`).

## 🚀 Usage

This project contains language-specific implementations for running evaluations. Please refer to the `README.md` file within each subdirectory for detailed setup and execution instructions.

## ✅ Evaluation Providers

-   **[LangSmith](./langsmith/README.md)**: Contains examples for running evaluations using LangSmith.
    -   [Python Implementation](./langsmith/python/README.md)
    -   [TypeScript Implementation](./langsmith/typescript/README.md)

-   **[Arize](./arize/README.md)**: Contains examples for running evaluations using Arize Phoenix.

-   **[Single vs Multi Agent](./single_vs_multi_agent/README.md)**: Specialized evaluations for comparing single-agent vs multi-agent performance configurations.


## 🏗️ Project Structure
- `langsmith/`
  - `python/`
    - `main.py`: Entry point for Python evaluations.
    - `config.py`: Configuration and environment variable handling.
    - `dataset.py`: Dataset loading and management.
    - `judge.py`: Evaluation and scoring logic.
    - `requirements.txt`: Python dependencies.
    - `README.md`: Python-specific setup and run instructions.
  - `typescript/`
    - `index.ts`: Entry point for TypeScript evaluations.
    - `config.ts`: Configuration and environment variable handling.
    - `dataset.ts`: Dataset loading and management.
    - `judge.ts`: Evaluation and scoring logic.
    - `package.json`: TypeScript dependencies.
    - `tsconfig.json`: TypeScript compiler options.
    - `README.md`: TypeScript-specific setup and run instructions.
  - `README.md`: Links to language-specific implementations.
- `arize/`
  - `main.py`: Entry point for Python evaluations with Arize.
  - `config.py`: Configuration and environment variable handling.
  - `dataset.py`: Dataset loading and management.
  - `judge.py`: Evaluation and scoring logic.
  - `requirements.txt`: Python dependencies.
  - `README.md`: Arize-specific setup and run instructions.
- `single_vs_multi_agent/`
  - `main.py`: Entry point for single vs multi agent comparison evaluations.
  - `config.py`: Configuration for single vs multi agent evaluations.
  - `requirements.txt`: Python dependencies.
  - `README.md`: Setup and usage instructions for single vs multi agent evaluations.
- `.env.example`: Example environment configuration.
- `README.md`: This file.

## 🙌 Contributing
Pull requests and issues are welcome! Please open an [issue](https://github.com/SonicDMG/evals_in_langflow/issues) to discuss your ideas or report bugs.

## 📜 License
This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).
