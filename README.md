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

Langflow agent evaluation framework with LangSmith integration.

## Overview

evals_in_langflow is a framework for evaluating Langflow agents using LangSmith. It provides a structured way to run, judge, and analyze agent outputs against datasets, making it easier to benchmark and improve your Langflow-based LLM applications.

## Features
- Run agent evaluations against datasets
- Integrate with LangSmith for tracing and analytics
- Configurable via environment variables
- Supports both Python and TypeScript ignores for clean development

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/SonicDMG/evals_in_langflow.git
   cd evals_in_langflow
   ```

2. **Set up a virtual environment (recommended):**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   - Copy `.env.example` to `.env` and fill in your API keys and project info.
   ```bash
   cp .env.example .env
   # Edit .env with your preferred editor
   ```

## Usage

To run the main evaluation script:
```bash
python main.py
```

- Make sure your `.env` file is properly configured with your API keys and project settings.
- Results and logs will be output to the console and/or as configured in your environment.

## Project Structure
- `main.py` – Entry point for running evaluations
- `config.py` – Configuration and environment variable handling
- `dataset.py` – Dataset loading and management
- `judge.py` – Evaluation and scoring logic
- `requirements.txt` – Python dependencies
- `.env.example` – Example environment configuration

## Contributing
Pull requests and issues are welcome! Please open an issue to discuss your ideas or report bugs.

## License
This project is licensed under the MIT License.
