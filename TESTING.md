# Testing Guide

This document provides comprehensive testing guidelines for contributors to the Django Model Populator project.

## Quick Start

### Running All Tests

```bash
python manage.py test
```

### Running Tests with Coverage

```bash
coverage run manage.py test
coverage report
coverage html  # Generate HTML coverage report
```

### Using Just Commands

If you have [just](https://github.com/casey/just) installed:

```bash
just setup-uv         # Quick setup with uv (fastest)
just setup-pip        # Setup with pip
just test             # Run all tests
just test-verbose     # Run with verbose output
just coverage         # Run tests with coverage report
just coverage-html    # Generate HTML coverage report
```

## Test Structure

The project has two main test suites:

### 1. Model Populator Tests (`model_populator/tests.py`)

Tests the core functionality of the fake data generation engine:

- **ModelPopulatorTestCase**: Core engine functionality
  - Single and multiple object generation
  - Unique field handling
  - Foreign key relationships
  - Field type generation (email, URL, date, decimal, etc.)
  - JSON field handling
  - Auto-timestamp fields
  - Related name access

- **FieldMappingTestCase**: Field mapping functionality
  - Phone number formatting
  - Address generation
  - Description fields

- **EdgeCaseTestCase**: Edge cases and error handling
  - Zero objects generation
  - Nullable/blank fields
  - Default values

### 2. Books Example App Tests (`books/tests.py`)

Tests the example application and demonstrates proper usage:

- **BooksExampleAppTestCase**: Basic model functionality
  - Model registration
  - Manual object creation
  - Relationships
  - String representations
  - Constraints (unique, cascade delete)

- **FakesManagementCommandTestCase**: Management command testing
  - Generate data for entire app
  - Generate data for specific models
  - Multiple model generation

## Running Specific Tests

### Run a specific test class:

```bash
python manage.py test model_populator.tests.ModelPopulatorTestCase
```

### Run a specific test method:

```bash
python manage.py test model_populator.tests.ModelPopulatorTestCase.test_generate_single_author
```

### Run tests from a specific app:

```bash
python manage.py test books
python manage.py test model_populator
```

### Run tests with verbose output:

```bash
python manage.py test --verbosity=2
```

## Example App (books/)

The `books/` directory contains a complete Django app that serves as:

1. **Example Usage**: Demonstrates how to use the model populator
2. **Test Fixtures**: Provides realistic models for testing
3. **Documentation**: Shows best practices

### Models Included:

- **Author**: Person who writes books
  - Unique name constraint
  - Email, website, bio fields
  - Date fields

- **Publisher**: Company that publishes books
  - Complex fields (JSON, URL, Boolean)
  - Contact information
  - Timestamps

- **Book**: The main entity
  - Foreign keys to Author and Publisher
  - Unique ISBN constraint
  - Various field types (decimal, integer, date, text)
  - Cascade delete behavior

## Writing New Tests

When contributing new features, follow these guidelines:

### 1. Test File Location

- Core engine tests: `model_populator/tests.py`
- Example/integration tests: `books/tests.py`

### 2. Test Structure

```python
from django.test import TestCase
from model_populator.engine import generate_fake_data
from books.models import YourModel

class YourFeatureTestCase(TestCase):
    def setUp(self):
        """Clean up before each test"""
        YourModel.objects.all().delete()
    
    def test_your_feature(self):
        """Test description"""
        # Arrange
        expected_count = 5
        
        # Act
        generate_fake_data(YourModel, num_objects=expected_count)
        
        # Assert
        self.assertEqual(YourModel.objects.count(), expected_count)
```

### 3. Test Coverage Guidelines

Aim for:
- **Core functionality**: 90%+ coverage
- **Edge cases**: Test error conditions
- **Integration**: Test with real Django models
- **Validation**: Verify data correctness, not just presence

### 4. What to Test

✅ **DO Test:**
- Field type generation correctness
- Unique constraint handling
- Relationship creation (ForeignKey, OneToOne, ManyToMany)
- Data validation (e.g., positive integers, valid URLs)
- Edge cases (zero objects, nullable fields, defaults)

❌ **DON'T Test:**
- Django's built-in functionality
- Third-party library internals (Faker)
- Database-specific behaviors

## Continuous Integration

Before submitting a pull request:

1. **Run all tests**: `python manage.py test`
2. **Check coverage**: `coverage run manage.py test && coverage report`
3. **Verify no errors**: Tests should pass with 0 failures
4. **Add new tests**: For any new features or bug fixes

## Manual Testing

You can also manually test the package:

### 1. Run Django Shell

```bash
python manage.py shell
```

### 2. Import and Test

```python
from model_populator.engine import generate_fake_data
from books.models import Author, Book, Publisher

# Generate some authors
generate_fake_data(Author, num_objects=5)

# Check the results
Author.objects.all()

# Generate books (will auto-create related models)
generate_fake_data(Book, num_objects=10)

# Inspect relationships
book = Book.objects.first()
print(f"Title: {book.title}")
print(f"Author: {book.author.name}")
print(f"Publisher: {book.publisher.name}")
```

### 3. Use Management Commands

```bash
# Generate data for all models in books app
python manage.py populate books --num 10

# Generate data for specific models
python manage.py populate books --models Author Publisher --num 5

# Generate data for all apps
python manage.py populate --all --num 20
```

## Troubleshooting Tests

### Database Issues

If tests fail due to database state:

```bash
# Delete the test database
rm db.sqlite3

# Run migrations
python manage.py migrate

# Try tests again
python manage.py test
```

### Import Errors

Make sure the project is in your Python path:

```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Faker Unique Constraint Errors

If you get `UniquenessException` from Faker:

- This is expected when generating many objects with unique fields
- The code handles this gracefully with `SafeUniqueProxy`
- Tests should verify unique fields don't cause failures

## Example Test Session

```bash
# 1. Set up environment (choose one method)

# Method 1: Using uv (fastest - recommended)
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

# Method 2: Using venv + pip
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Method 3: Using just
just setup-uv  # or: just setup-pip

# 2. Run migrations
python manage.py migrate

# 3. Run all tests
python manage.py test

# 4. Run with coverage
coverage run manage.py test
coverage report
coverage html

# 5. Open coverage report
open htmlcov/index.html

# 6. Run specific test suite
python manage.py test model_populator.tests.ModelPopulatorTestCase

# 7. Manual verification
python manage.py shell
>>> from model_populator.engine import generate_fake_data
>>> from books.models import Book
>>> generate_fake_data(Book, num_objects=5)
>>> Book.objects.all()
```

## Contributing Tests

When submitting a PR:

1. **Add tests for new features**: Every new feature should have corresponding tests
2. **Update existing tests**: If you change behavior, update affected tests
3. **Document test purpose**: Use clear docstrings
4. **Ensure tests pass**: All tests must pass before merging
5. **Maintain coverage**: Don't decrease overall test coverage

## Questions?

If you have questions about testing:

1. Check existing tests for examples
2. Review the Django testing documentation
3. Open an issue on GitHub
4. Look at the example app (`books/`) for patterns
