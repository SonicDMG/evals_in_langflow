# Test Structure

This directory contains the test files for the single vs multi agent evaluation project. The tests have been separated into two categories for better organization and faster execution.

## Test Files

### `test_unit.py` - Unit Tests
- **Purpose**: Test individual functions with mocked dependencies
- **Scope**: Fast, isolated testing of function logic
- **Dependencies**: All external calls are mocked
- **Execution Time**: Very fast (milliseconds)
- **Use Case**: Development, CI/CD, quick validation

**What's Tested**:
- `call_langflow_api()` function with mocked HTTP responses
- `create_ls_target()` function
- Configuration constants
- Error handling scenarios
- Mocked dataset operations

### `test_integration.py` - Integration Tests
- **Purpose**: Test the full workflow with real external dependencies
- **Scope**: End-to-end testing with real LangSmith datasets
- **Dependencies**: Real LangSmith client, real Math Dataset
- **Execution Time**: Slower (depends on external services)
- **Use Case**: Full validation, pre-deployment testing

**What's Tested**:
- Real dataset loading and validation
- Full API call workflows
- Dataset structure validation
- Metadata handling with real data
- Endpoint configuration validation

### `test_single_vs_multi_agent.py` - Deprecated
- **Status**: Deprecated - replaced by the above files
- **Action**: Will be removed in future versions

## Running Tests

### Run All Tests
```bash
pytest tests/
```

### Run Only Unit Tests (Fast)
```bash
pytest tests/test_unit.py
```

### Run Only Integration Tests
```bash
pytest tests/test_integration.py
```

### Run Tests by Category
```bash
# Unit tests only
pytest -m unit

# Integration tests only
pytest -m integration

# LangSmith tests only
pytest -m langsmith
```

### Run Tests with Verbose Output
```bash
pytest -v tests/
```

## Test Markers

The tests use pytest markers to categorize them:

- `@pytest.mark.unit`: Unit tests (fast, mocked)
- `@pytest.mark.integration`: Integration tests (slower, real dependencies)
- `@pytest.mark.langsmith`: Tests that use LangSmith features
- `@pytest.mark.slow`: Tests that take longer to run

## Configuration

The test configuration is defined in `pytest.ini` at the project root. Key settings:

- `testpaths = tests`: Test discovery directory
- `python_files = test_*.py`: Test file pattern
- `python_classes = Test*`: Test class pattern
- `python_functions = test_*`: Test function pattern

## Best Practices

1. **Unit Tests First**: Always run unit tests during development for fast feedback
2. **Integration Tests for Validation**: Run integration tests before committing major changes
3. **Mock External Dependencies**: Unit tests should never make real API calls
4. **Use Appropriate Markers**: Mark tests appropriately for selective execution
5. **Keep Tests Fast**: Unit tests should complete in under 1 second

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure you're running tests from the project root directory
2. **Mock Issues**: Check that all external dependencies are properly mocked in unit tests
3. **Dataset Loading**: Integration tests require access to the Math Dataset in LangSmith
4. **API Keys**: Ensure environment variables are set for integration tests

### Debug Mode

Run tests with debug output:
```bash
pytest -v --tb=long tests/
```

### Skip Integration Tests

If you only want to run unit tests:
```bash
pytest -m "not integration" tests/
```

