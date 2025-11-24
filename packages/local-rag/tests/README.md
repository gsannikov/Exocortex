# Tests for 2ndBrain_RAG

This directory contains the test suite for the 2ndBrain_RAG project.

## Running Tests

### Quick Start

Run all tests:
```bash
pytest
```

Run tests with verbose output:
```bash
pytest -v
```

Run tests with coverage:
```bash
pytest --cov=mcp_server --cov=ingest --cov-report=html --cov-report=term-missing
```

### Installation

Install test dependencies:
```bash
pip install -r requirements-test.txt
```

Or install all dependencies including tests:
```bash
pip install -r requirements.txt
pip install -r requirements-test.txt
```

## Test Structure

```
tests/
├── __init__.py           # Package initialization
├── conftest.py           # Pytest fixtures and configuration
├── test_mcp_server.py    # Tests for mcp_server.py
├── test_extractor.py     # Tests for ingest/extractor.py
└── test_ocr.py           # Tests for ingest/ocr.py
```

## Test Categories

### Unit Tests

Test individual functions and methods in isolation:
```bash
pytest -v tests/test_mcp_server.py
```

### Integration Tests

Test interactions between components:
```bash
pytest -m integration
```

### Slow Tests

Skip slow tests during development:
```bash
pytest -m "not slow"
```

## Coverage Reports

Generate HTML coverage report:
```bash
pytest --cov=mcp_server --cov=ingest --cov-report=html
```

View the report:
```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

## Writing Tests

### Test Naming Convention

- Test files: `test_*.py`
- Test classes: `Test*`
- Test functions: `test_*`

### Using Fixtures

Common fixtures are defined in `conftest.py`:

```python
def test_example(temp_dir, sample_text_file):
    """Test using fixtures."""
    assert sample_text_file.exists()
    assert sample_text_file.parent == temp_dir
```

### Parametrized Tests

Test multiple scenarios:

```python
@pytest.mark.parametrize("size,overlap", [
    (1000, 100),
    (500, 50),
])
def test_chunking(size, overlap):
    """Test with different parameters."""
    # test code
```

## Test Markers

Available markers (defined in `pytest.ini`):

- `@pytest.mark.slow` - Slow running tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.requires_models` - Tests that need ML models

## CI/CD

Tests run automatically on:
- Every push to main/master
- Every pull request

See `.github/workflows/ci.yml` for CI configuration.

## Troubleshooting

### Import Errors

If you get import errors, make sure you're running from the project root:
```bash
cd /path/to/2ndBrain_RAG
pytest
```

### Missing Dependencies

Install all test dependencies:
```bash
pip install -r requirements-test.txt
```

### Slow Tests

Skip slow tests:
```bash
pytest -m "not slow"
```

Or run only fast tests:
```bash
pytest -m "not slow and not integration"
```

## Coverage Goals

Target coverage levels:
- **Overall**: 70%+
- **Core modules** (`mcp_server.py`): 80%+
- **Utility modules** (`ingest/`): 70%+

Current coverage can be checked by running:
```bash
pytest --cov=mcp_server --cov=ingest --cov-report=term-missing
```

## Contributing

When adding new features:
1. Write tests first (TDD approach recommended)
2. Ensure tests pass: `pytest`
3. Check coverage: `pytest --cov`
4. Run linting: `ruff check .`

See [coding-conventions.md](../docs/coding-conventions.md) for more details.

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Pytest Fixtures](https://docs.pytest.org/en/stable/fixture.html)
- [Coverage.py](https://coverage.readthedocs.io/)
