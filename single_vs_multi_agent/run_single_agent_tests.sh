#!/bin/bash

# Run Single Agent Integration Tests with Custom Experiment Name
echo "Running Single Agent Integration Tests..."

export COLUMNS=150
LANGSMITH_TEST_SUITE="single-vs-multi-agent-comparison" \
LANGSMITH_EXPERIMENT="single-agent-qwen-qwen3-4b-2507-integration" \
python3 -m pytest -k "test_single_agent" tests/test_integration.py -v --langsmith-output

echo "Single Agent Integration Tests Complete!"