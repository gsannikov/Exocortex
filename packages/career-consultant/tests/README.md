# Test Suite Documentation

## Overview

This directory contains the comprehensive test suite for the Israeli Tech Career Consultant project. The tests ensure code quality, prevent regressions, and validate critical business logic.

## Test Structure

```
tests/
├── conftest.py              # Shared pytest fixtures
├── unit/                    # Unit tests for individual modules
│   ├── test_cv_matcher.py   # CV matching & scoring logic (76 tests)
│   ├── test_yaml_utils.py   # YAML frontmatter handling (60+ tests)
│   ├── test_slug_utils.py   # Slug generation & validation (80+ tests)
│   └── ...
├── integration/             # Integration tests
│   └── ...
└── fixtures/                # Test data and fixtures
```

## Running Tests

### Run All Tests

```bash
pytest
```

### Run Specific Test File

```bash
pytest tests/unit/test_cv_matcher.py
```

### Run Specific Test Class

```bash
pytest tests/unit/test_cv_matcher.py::TestCalculateMatchScore
```

### Run Specific Test

```bash
pytest tests/unit/test_cv_matcher.py::TestCalculateMatchScore::test_perfect_match
```

### Run with Coverage

```bash
pytest --cov=skill-package/scripts --cov=host_scripts --cov-report=html
```

Then open `htmlcov/index.html` in your browser to view the coverage report.

### Run with Verbose Output

```bash
pytest -v
```

### Run Only Fast Tests (exclude slow tests)

```bash
pytest -m "not slow"
```

## Test Categories

### Unit Tests (`tests/unit/`)

Test individual functions and classes in isolation.

**Priority Modules:**
- **`test_cv_matcher.py`** - CRITICAL: Tests CV matching and scoring logic
- **`test_yaml_utils.py`** - HIGH: Tests YAML frontmatter handling
- **`test_slug_utils.py`** - HIGH: Tests slug generation and validation
- **`test_config_loader.py`** - HIGH: Tests configuration loading
- **`test_versioning.py`** - MEDIUM: Tests version management

### Integration Tests (`tests/integration/`)

Test complete workflows and interactions between components.

**Planned Tests:**
- Full job analysis workflow
- Excel generation from YAML
- Migration scripts
- File I/O operations

## Writing Tests

### Test Naming Convention

```python
class TestFunctionName:
    """Test suite for function_name()."""

    def test_basic_functionality(self):
        """Test basic use case."""
        pass

    def test_edge_case_empty_input(self):
        """Test handling of empty input."""
        pass

    def test_error_invalid_input(self):
        """Test error handling for invalid input."""
        pass
```

### Using Fixtures

Fixtures are defined in `conftest.py` and can be used by any test:

```python
def test_with_sample_data(sample_cv_content, sample_config):
    """Test using pre-defined sample data."""
    # sample_cv_content and sample_config are automatically provided
    assert "Python" in sample_cv_content
```

### Available Fixtures

- `sample_cv_content` - Sample EM CV content
- `sample_cv_tpm` - Sample TPM CV content
- `sample_job_requirements_senior_em` - Sample job requirements
- `sample_config` - Complete user configuration
- `sample_company_frontmatter` - Company YAML data
- `sample_role_frontmatter` - Role YAML data
- `temp_user_data_dir` - Temporary user-data directory

### Testing Best Practices

1. **Test One Thing** - Each test should verify one specific behavior
2. **Use Descriptive Names** - Test names should explain what they test
3. **Arrange-Act-Assert** - Structure tests clearly:
   ```python
   def test_calculate_score():
       # Arrange
       cv = "Python, AWS"
       job = "Python Engineer"

       # Act
       score = calculate_match_score(job, cv, "Engineering")

       # Assert
       assert score > 0
   ```
4. **Test Edge Cases** - Empty inputs, very large inputs, Unicode, etc.
5. **Test Error Conditions** - Verify proper error handling
6. **Don't Repeat Yourself** - Use fixtures for common setup

## Coverage Goals

| Module | Target Coverage | Current | Priority |
|--------|----------------|---------|----------|
| cv_matcher.py | 95%+ | 🔴 TBD | CRITICAL |
| yaml_utils.py | 90%+ | 🔴 TBD | HIGH |
| slug_utils.py | 90%+ | 🔴 TBD | HIGH |
| config_loader.py | 90%+ | 🔴 TBD | HIGH |
| versioning.py | 85%+ | 🔴 TBD | MEDIUM |

**Overall Goal:** 80%+ coverage across all critical modules

## Continuous Integration

Tests run automatically on:
- Every push to `main` or `claude/*` branches
- Every pull request to `main`

The CI pipeline:
1. Runs tests on Python 3.8, 3.9, 3.10, 3.11
2. Measures code coverage
3. Uploads coverage reports to Codecov
4. Runs code linting (flake8, black)
5. Fails if coverage drops below 70%

## Debugging Failed Tests

### View Test Output

```bash
pytest -v --tb=short
```

### Stop on First Failure

```bash
pytest -x
```

### Drop into Debugger on Failure

```bash
pytest --pdb
```

### Print Debug Output

```bash
pytest -s  # Shows print statements
```

### Run Last Failed Tests

```bash
pytest --lf
```

## Test Markers

Mark tests with decorators for categorization:

```python
@pytest.mark.unit
def test_unit():
    pass

@pytest.mark.integration
def test_integration():
    pass

@pytest.mark.slow
def test_slow_operation():
    pass
```

Run specific markers:
```bash
pytest -m unit        # Run only unit tests
pytest -m integration # Run only integration tests
pytest -m "not slow"  # Skip slow tests
```

## Adding New Tests

### Checklist for New Tests

- [ ] Test file named `test_*.py`
- [ ] Test classes named `Test*`
- [ ] Test functions named `test_*`
- [ ] Docstrings explain what is tested
- [ ] Edge cases covered
- [ ] Error conditions tested
- [ ] Fixtures used for common setup
- [ ] Tests pass locally before committing

### Example: Adding Tests for New Module

1. Create test file: `tests/unit/test_new_module.py`

```python
"""Tests for new_module.py"""

import pytest
import new_module


class TestNewFunction:
    """Test suite for new_function()."""

    def test_basic_usage(self):
        """Test basic functionality."""
        result = new_module.new_function("input")
        assert result == "expected"

    def test_edge_case(self):
        """Test edge case."""
        result = new_module.new_function("")
        assert result is not None
```

2. Run tests:
```bash
pytest tests/unit/test_new_module.py -v
```

3. Check coverage:
```bash
pytest tests/unit/test_new_module.py --cov=new_module --cov-report=term-missing
```

## Common Issues

### Import Errors

If you get import errors:
```bash
# Add skill-package/scripts to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/skill-package/scripts"
pytest
```

Or use the pytest configuration in `conftest.py` which adds paths automatically.

### Fixture Not Found

Ensure fixtures are defined in:
- `conftest.py` (for project-wide fixtures)
- Same test file (for test-specific fixtures)

### Tests Fail in CI but Pass Locally

Common causes:
- Different Python version
- Missing dependencies
- File system differences
- Timezone differences

Fix by running tests with the same Python version as CI:
```bash
python3.11 -m pytest
```

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest fixtures](https://docs.pytest.org/en/stable/fixture.html)
- [pytest markers](https://docs.pytest.org/en/stable/mark.html)
- [Coverage.py](https://coverage.readthedocs.io/)

## Contributing

When adding new features:
1. Write tests first (TDD approach recommended)
2. Ensure tests pass locally
3. Achieve target coverage for new code
4. Update this README if adding new test categories

## Questions?

If you have questions about testing:
1. Check this README
2. Look at existing tests for examples
3. Open an issue on GitHub
4. Refer to CLAUDE.md for AI assistant guidelines

---

**Last Updated:** 2025-11-18
**Test Count:** 200+ tests
**Coverage Goal:** 80%+
