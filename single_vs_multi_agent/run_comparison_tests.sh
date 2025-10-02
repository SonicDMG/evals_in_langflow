#!/bin/bash

# Run Both Single and Multi Agent Tests for Comparison
echo "Running Single vs Multi Agent Comparison Tests..."

export COLUMNS=150

echo "=== Running Single Agent Tests ==="
LANGSMITH_TEST_SUITE="single-vs-multi-agent-comparison" \
LANGSMITH_EXPERIMENT="single-agent-qwen-qwen3-4b-2507-integration" \
python3 -m pytest -k "test_single_agent" tests/test_integration.py -v --langsmith-output

echo ""
echo "=== Running Multi Agent Tests ==="  
LANGSMITH_TEST_SUITE="single-vs-multi-agent-comparison" \
LANGSMITH_EXPERIMENT="multi-agent-qwen-qwen3-4b-2507-integration" \
python3 -m pytest -k "test_multi_agent" tests/test_integration.py -v --langsmith-output

echo ""
echo "Comparison Tests Complete!"
echo "Check LangSmith for experiment results:"
echo "- single-agent-qwen-qwen3-4b-2507-integration" 
echo "- multi-agent-qwen-qwen3-4b-2507-integration"