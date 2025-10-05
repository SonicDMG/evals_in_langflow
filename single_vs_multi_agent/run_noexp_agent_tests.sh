#!/bin/bash

# Run No Explanation Agent Integration Tests with Custom Experiment Name
echo "Running No Explanation Agent Integration Tests..."

export COLUMNS=150
LANGSMITH_TEST_SUITE="single-vs-multi-agent-comparison" \
LANGSMITH_EXPERIMENT="noexp-agent-qwen-qwen3-4b-2507-integration" \
python3 -m pytest -k "test_noexp_agent" tests/test_integration.py -v --langsmith-output

echo "No Explanation Agent Integration Tests Complete!"