# Summit Agents Backend Test Suite

This directory contains the test suite for the Summit Agents backend application.

## Test Structure

```
tests/
├── api/                    # API endpoint tests
│   └── v1/
│       ├── test_auth.py   # Authentication endpoint tests
│       ├── test_business.py # Business management tests
│       └── test_surveys.py  # Survey management tests
├── core/                   # Core module tests
│   ├── test_config.py     # Configuration tests
│   └── test_security.py   # Security module tests
├── db/                    # Database tests
│   └── test_base.py      # Database base module tests
├── performance/          # Performance tests
│   └── test_api_performance.py # API performance tests
├── conftest.py          # Test configuration and fixtures
├── factories.py         # Test data factories
└── README.md           # This file
```

## Test Categories

The test suite uses pytest markers to categorize tests:

- `unit`: Unit tests for individual components
- `integration`: Integration tests between components
- `api`: API endpoint tests
- `db`: Database-related tests
- `auth`: Authentication and authorization tests
- `performance`: Performance and load tests
- `slow`: Tests that take longer to run
- `security`: Security-related tests

## Running Tests

### Basic Test Run
```bash
poetry run pytest
```

### Run Specific Test Categories
```bash
# Run only unit tests
poetry run pytest -m unit

# Run only API tests
poetry run pytest -m api

# Run performance tests
poetry run pytest -m performance

# Exclude slow tests
poetry run pytest -m "not slow"
```

### Test Coverage
```bash
# Run tests with coverage report
poetry run pytest --cov=app --cov-report=term-missing

# Generate HTML coverage report
poetry run pytest --cov=app --cov-report=html
```

### Parallel Test Execution
```bash
# Run tests in parallel
poetry run pytest -n auto
```

## Test Data

The test suite uses factory_boy to generate test data. Test factories are defined in `factories.py`:

- `BusinessFactory`: Creates test business instances
- `UserFactory`: Creates test user instances
- `SuperUserFactory`: Creates test superuser instances
- `SurveyResponseFactory`: Creates test survey responses

## Test Configuration

Test configuration is managed through:

1. `conftest.py`: Contains pytest fixtures and setup
2. `pyproject.toml`: Contains pytest settings and markers
3. Environment variables: Test-specific settings

### Required Environment Variables

```env
TEST_DATABASE_URL=postgresql://user:pass@localhost:5432/test_db
REDIS_URL=redis://localhost:6379/1
SECRET_KEY=test_secret_key_123
ENVIRONMENT=test
```

## Performance Testing

Performance tests measure:

- Response times
- Concurrent request handling
- Resource utilization (CPU, memory)
- API endpoint performance under load

Performance test thresholds:

- Average response time: < 500ms
- 95th percentile: < 1s
- Maximum response time: < 2s
- CPU usage increase: < 70%
- Memory usage increase: < 20%

## Adding New Tests

1. Place tests in appropriate directory based on component
2. Use relevant pytest markers
3. Create fixtures in `conftest.py` if needed
4. Add factories for new models in `factories.py`
5. Follow existing test patterns and naming conventions
6. Include docstrings and comments
7. Ensure proper error handling
8. Add performance tests for new endpoints

## Best Practices

1. Use async/await for all async operations
2. Use fixtures for test data and setup
3. Clean up test data after tests
4. Keep tests focused and atomic
5. Use meaningful test names
6. Include both positive and negative test cases
7. Test edge cases and error conditions
8. Monitor test performance

## Continuous Integration

The test suite is run on every pull request and merge to main:

1. Unit and integration tests
2. Coverage report generation
3. Performance test baseline checks
4. Security test verification

## Troubleshooting

Common issues and solutions:

1. Database connection errors:
   - Verify TEST_DATABASE_URL is correct
   - Ensure test database exists
   - Check database permissions

2. Slow tests:
   - Use pytest-xdist for parallel execution
   - Mark slow tests appropriately
   - Optimize database operations

3. Flaky tests:
   - Check for race conditions
   - Verify proper cleanup
   - Ensure proper async handling 