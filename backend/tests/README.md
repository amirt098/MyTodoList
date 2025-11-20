# Tests Directory

This directory contains end-to-end tests for the My Todo List backend application.

## Structure

```
tests/
├── __init__.py
├── conftest.py              # Optional pytest configuration (for future use)
├── test_project_e2e.py      # End-to-end tests for Project models and processes
├── README.md               # This file
├── run_tests.sh            # Test runner script (Linux/Mac)
└── run_tests.bat           # Test runner script (Windows)
```

## Test Framework

Tests use **Django's TestCase** which provides:
- Automatic database setup and teardown
- Transaction rollback after each test
- Test client for API testing
- Isolated test execution

All services are imported from `runner.bootstrap` to ensure tests use the same dependency injection setup as the application.

## Test Coverage

### `test_project_e2e.py`

Comprehensive end-to-end tests covering:

1. **Model Tests**
   - Project model creation and operations
   - ProjectMember model creation and operations

2. **Repository Service Tests**
   - Project CRUD operations
   - Project member management operations

3. **UseCase Service Tests**
   - Project management business logic
   - Access control and permissions
   - Member role management

4. **REST API Tests**
   - All project endpoints
   - All member management endpoints
   - Error handling

5. **Full Workflow Test**
   - Complete end-to-end workflow from API to database
   - Multi-step operations verification

## Running Tests

### Prerequisites

Make sure you have the required dependencies installed:

```bash
pip install -r requirements.txt
```

### Run All Tests

```bash
python manage.py test tests
```

### Run Specific Test File

```bash
python manage.py test tests.test_project_e2e
```

### Run Specific Test Class

```bash
python manage.py test tests.test_project_e2e.ProjectEndToEndTest
```

### Run Specific Test Method

```bash
python manage.py test tests.test_project_e2e.ProjectEndToEndTest.test_full_workflow_e2e
```

### Using pytest (if installed)

```bash
pytest tests/
```

## Test Database

Tests use a separate test database (SQLite in-memory by default) that is automatically created and destroyed for each test run. No data from your development database will be affected.

## Test Structure

Each test method:
- Uses Django's `TestCase` for automatic database management
- Sets up test data in `setUp()` method
- Uses services from `bootstrapper` (same as production)
- Tests a specific functionality
- Verifies results at multiple layers (API, UseCase, Repository, Database)
- Cleans up automatically after execution (Django handles this)

## Key Features

- **Uses Django TestCase**: Automatic database transaction management
- **Uses Bootstrapper**: Tests use the same services as production via `runner.bootstrap`
- **Isolated Tests**: Each test runs in its own transaction that's rolled back
- **Multi-layer Verification**: Tests verify at Model, Repository, UseCase, and API layers

## Adding New Tests

When adding new tests:

1. Follow the existing test structure
2. Use descriptive test method names starting with `test_`
3. Test at multiple layers (Model → Repository → UseCase → API)
4. Include both success and failure scenarios
5. Verify database state after operations

## Notes

- All tests use Django's TestCase which provides database transaction rollback
- Tests are isolated - each test runs in its own transaction
- Timestamps are generated using DateTimeService
- User IDs are test integers (1, 2, 3, etc.)

