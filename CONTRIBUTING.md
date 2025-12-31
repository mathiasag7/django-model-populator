# Contributing to Django Model Populator

Thank you for your interest in contributing to Django Model Populator! This guide will help you get started.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Development Setup](#development-setup)
3. [Running Tests](#running-tests)
4. [Making Changes](#making-changes)
5. [Code Style](#code-style)
6. [Submitting Changes](#submitting-changes)
7. [Example Application](#example-application)

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment tool (venv, virtualenv, conda, or [uv](https://github.com/astral-sh/uv))

> **Installing uv**: For the fastest setup, install uv with:
> ```bash
> # macOS/Linux
> curl -LsSf https://astral.sh/uv/install.sh | sh
> 
> # Windows
> powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
> 
> # Or via pip
> pip install uv
> ```

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:

```bash
git clone https://github.com/mathiasag07/django_model_populator.git
cd django_model_populator
```

## Development Setup

> **💡 Tip**: This project supports multiple Python environment managers. We recommend [uv](https://github.com/astral-sh/uv) for the fastest setup experience (~10x faster than pip).

### 1. Create and Activate Virtual Environment

```bash
# Using uv (fastest option - recommended)
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Using venv (Python 3)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Using conda
conda create -n django_populator python=3.11
conda activate django_populator
```

### 2. Install Dependencies

```bash
# Using uv (fastest option - recommended)
uv pip install -r requirements.txt
# Or install the package in development mode
uv pip install -e .

# Using pip
pip install -r requirements.txt
# Or install the package in development mode
pip install -e .

# Using conda
conda install --file requirements.txt
```

### 3. Run Initial Migrations

```bash
python manage.py migrate
```

### 4. Verify Installation

```bash
# Check that everything works
python manage.py check

# Try generating some fake data
python manage.py populate books --num 5
```

## Running Tests

### Quick Test Run

```bash
# Run all tests
python manage.py test

# Run with verbose output
python manage.py test --verbosity=2
```

### Using Just Commands

If you have [just](https://github.com/casey/just) installed:

```bash
just test              # Run all tests
just test-verbose      # Run with verbose output
just coverage          # Run with coverage report
just coverage-html     # Generate HTML coverage report
```

### Test Specific Components

```bash
# Test model populator only
python manage.py test model_populator

# Test example app only
python manage.py test books

# Test specific class
python manage.py test model_populator.tests.ModelPopulatorTestCase

# Test specific method
python manage.py test model_populator.tests.ModelPopulatorTestCase.test_unique_field_handling
```

### Coverage Reports

```bash
# Run tests with coverage
coverage run manage.py test

# View coverage report in terminal
coverage report

# Generate HTML coverage report
coverage html
open htmlcov/index.html  # On macOS
# Or navigate to htmlcov/index.html in your browser
```

## Making Changes

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

### 2. Make Your Changes

Key areas you might work on:

#### Adding Support for New Field Types

Edit [model_populator/field_mappings.py](model_populator/field_mappings.py):

```python
# Add to FIELD_TYPE_MAPPING
FIELD_TYPE_MAPPING = {
    # ... existing mappings ...
    "YourCustomField": [
        {"faker": "your_faker_method"},
    ],
}
```

#### Improving Field Name Recognition

Edit [model_populator/field_mappings.py](model_populator/field_mappings.py):

```python
# Add to FIELD_NAME_MAPPING
FIELD_NAME_MAPPING = {
    # ... existing mappings ...
    "your_faker_method": ["field_name1", "field_name2"],
}
```

#### Modifying Core Generation Logic

Edit [model_populator/engine.py](model_populator/engine.py):

- `generate_fake_data()`: Main generation function
- `_get_fake_value_based_on_type()`: Type-based value generation
- `_get_fake_char_value()`: CharField-specific logic
- `_set_m2m_objects()`: ManyToMany relationship handling

### 3. Add Tests

**Always add tests for new features!**

#### For Engine Changes

Add tests to [model_populator/tests.py](model_populator/tests.py):

```python
def test_your_new_feature(self):
    """Test description"""
    # Arrange
    from model_populator.engine import generate_fake_data
    from books.models import YourModel
    
    # Act
    generate_fake_data(YourModel, num_objects=5)
    
    # Assert
    self.assertEqual(YourModel.objects.count(), 5)
    # Add more specific assertions
```

#### For Integration Testing

Use the example app in [books/tests.py](books/tests.py):

```python
def test_integration_scenario(self):
    """Test end-to-end functionality"""
    # Use the books models to test real-world scenarios
    pass
```

### 4. Test Your Changes

```bash
# Run all tests
python manage.py test

# Test with the example app
python manage.py shell
>>> from model_populator.engine import generate_fake_data
>>> from books.models import Book
>>> generate_fake_data(Book, num_objects=10)
>>> Book.objects.all()
```

### 5. Update Documentation

- Update [README.md](README.md) if you've added user-facing features
- Update [TESTING.md](TESTING.md) if you've changed test structure
- Update [books/README.md](books/README.md) if example app changes
- Add docstrings to new functions/classes
- Update [CHANGELOG.md](CHANGELOG.md)

## Code Style

### Python Style Guidelines

- Follow [PEP 8](https://pep8.org/)
- Use meaningful variable and function names
- Add docstrings to all public functions and classes
- Keep functions focused and single-purpose

### Example Docstring Format

```python
def generate_fake_data(model, fields: list = [], num_objects: int = 1):
    """
    Fills a specific model with fake data.

    :param model: Model class to fill with fake data.
    :param fields: List of fields to fill, if empty all fields will be filled.
    :param num_objects: Number of objects to generate.
    :return: The created object.
    :raises ValueError: If the model is not registered in Django.
    :example:
        from my_app.models import MyModel
        generate_fake_data(MyModel, num_objects=10)
    """
    pass
```

### Code Formatting

```bash
# Install formatters (if not already installed)
uv pip install black flake8  # or: pip install black flake8

# Format your code
black model_populator/

# Check for issues
flake8 model_populator/
```

## Submitting Changes

### 1. Commit Your Changes

```bash
git add .
git commit -m "Brief description of your changes"
```

**Commit Message Guidelines:**
- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- First line should be 50 characters or less
- Reference issues if applicable: "Fix #123: Handle edge case"

Examples:
```
Add support for custom JSONField handling
Fix unique constraint violation in CharField
Improve test coverage for relationship handling
Update documentation for field mappings
```

### 2. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 3. Create a Pull Request

1. Go to the original repository on GitHub
2. Click "New Pull Request"
3. Select your fork and branch
4. Fill in the PR template:

```markdown
## Description
Brief description of what this PR does

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] All tests pass
- [ ] Added new tests for this feature
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Added/updated documentation
- [ ] Updated CHANGELOG.md
- [ ] No unnecessary debug code or comments
```

### 4. Code Review Process

- Maintainers will review your PR
- Address any requested changes
- Once approved, your PR will be merged!

## Example Application

The [books/](books/) directory contains a complete example Django app for testing and development:

### Using the Example App

```bash
# Generate fake data
python manage.py populate books --num 10

# Test specific models
python manage.py populate books --models Author --num 20

# Explore in shell
python manage.py shell
>>> from books.models import Book, Author, Publisher
>>> Book.objects.all()
>>> Author.objects.all()
```

### Adding Test Models

If you need to test a new field type or pattern:

1. Add a model to [books/models.py](books/models.py)
2. Create and run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
3. Add tests to [books/tests.py](books/tests.py)
4. Test the generation:
   ```bash
   python manage.py populate books --models YourNewModel --num 5
   ```

## Common Development Tasks

### Add a New Faker Provider

```python
# In field_mappings.py
FIELD_TYPE_MAPPING = {
    "YourField": [
        {"faker": "your_provider_method"},
    ],
}

# In engine.py (if special handling needed)
def _get_fake_your_field_value(fake, mapping, field):
    # Custom logic here
    return getattr(fake, mapping[0]["faker"])()
```

### Debug Test Failures

```bash
# Run specific failing test
python manage.py test model_populator.tests.ModelPopulatorTestCase.test_your_failing_test --verbosity=2

# Use Django shell to reproduce issue
python manage.py shell
>>> from model_populator.engine import generate_fake_data
>>> from books.models import YourModel
>>> generate_fake_data(YourModel, num_objects=1)
```

### Clear Test Database

```bash
# Remove test artifacts
rm db.sqlite3

# Recreate database
python manage.py migrate
```

## Getting Help

- **Documentation**: Check [README.md](README.md) and [TESTING.md](TESTING.md)
- **Issues**: Search [existing issues](https://github.com/YOUR_ORG/django_model_populator/issues)
- **Questions**: Open a new issue with the "question" label
- **Discussions**: Start a discussion in GitHub Discussions

## Recognition

Contributors are recognized in:
- [CHANGELOG.md](CHANGELOG.md) for their contributions
- GitHub's contributors page
- Release notes

Thank you for contributing! 🎉
