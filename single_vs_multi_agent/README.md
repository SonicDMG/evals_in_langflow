# Single vs Multi Agent Evaluation

This directory contains specialized evaluation scripts for comparing single-agent vs multi-agent performance in Langflow flows.

## Overview

The scripts in this directory are designed to:
- Compare performance between single-agent and multi-agent configurations
- Evaluate different LLM models across both configurations
- Use LangSmith for tracing and evaluation
- Support math-specific evaluations with metadata handling

## Files

- `main.py` - Main evaluation script for single vs multi agent comparison
- `config.py` - Configuration and environment setup
- `requirements.txt` - Python dependencies
- `tests/` - Pytest test suite with LangSmith integration
- `validate_setup.py` - Environment validation script
- `README.md` - This file

## Usage

### Running Evaluations
1. Set up your environment variables in the root `.env` file
2. Install dependencies: `pip install -r requirements.txt`
3. Run the evaluation: `python main.py`

### Validating Your Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Validate environment: `python validate_setup.py`

### Running Tests with LangSmith Integration
1. Install dependencies: `pip install -r requirements.txt`
2. Run tests: `pytest tests/ --langsmith-output`

### Test Features
- **LangSmith Integration**: All tests automatically sync to LangSmith datasets
- **Mocked API Calls**: Tests run without hitting real Langflow endpoints
- **Rich Output**: Use `--langsmith-output` for detailed LangSmith results
- **Caching**: API responses are cached to avoid repeated calls
- **Test Suite**: Tests are grouped under "Single vs Multi Agent Evaluation"

## Configuration

The script is configured to test different LLM providers and models. You can modify the `MODELS_TO_TEST` list in `config.py` to test different models.

## Endpoints

The script tests two main endpoints:
- `math_eval_single_lms` - Single agent math evaluation
- `math_eval_multi_lms` - Multi agent math evaluation

## Dependencies

- langsmith
- python-dotenv
- requests
- rich

