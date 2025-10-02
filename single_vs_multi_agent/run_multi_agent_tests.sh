#!/bin/bash

# Run Multi Agent Integration Tests with Custom Experiment Name
echo "Running Multi Agent Integration Tests..."

export COLUMNS=150
LANGSMITH_TEST_SUITE="single-vs-multi-agent-comparison" \
LANGSMITH_EXPERIMENT="multi-agent-qwen-qwen3-4b-2507-integration" \
python3 -m pytest -k "test_multi_agent" tests/test_integration.py -v --langsmith-output

echo "Multi Agent Integration Tests Complete!"