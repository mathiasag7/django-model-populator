# Django Fake Filler

A Django application for automatically generating fake/dummy data for your Django models using the Faker library.

## The Story
This project was born from a very practical problem encountered while testing Django applications.

When generating test data, related objects were often recreated every time they were needed. Creating a book would automatically create a new author, even when an author already existed. Over time, this led to unrealistic databases filled with duplicated data and relationships that don’t reflect how real systems work

We wanted to create a tool that generates data mirroring real-world patterns.

## Built With Gratitude

This project stands on the shoulders of giants. Special thanks to:

**[Faker](https://github.com/joke2k/faker)** by Daniele Faraglia - The incredible Python library that powers all our fake data generation. Without Faker's comprehensive providers and localization support, this project wouldn't exist. 🙏

## Features

- 🎯 **Automatic Data Generation**: Intelligently generates fake data based on field names and types
- 🔗 **Relationship Support**: Handles ForeignKey, OneToOne, and ManyToMany relationships
- 🎨 **Field Mapping**: Smart field name detection (email, username, phone, etc.)
- ⚙️ **Customizable**: Configure field mappings and excluded models
- 📊 **Progress Tracking**: Built-in progress bars with tqdm
- 🛡️ **Safe Unique Fields**: Handles unique constraints gracefully

## Installation

Install from PyPI:

```bash
pip install django_model_populator
```

Add to your Django project's `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ... other apps
    'model_populator',
]
```

## Quick Start

### Generate Fake Data for All Models

```bash
python manage.py populate --all --num 10
```

### Generate Data for Specific App

```bash
python manage.py populate myapp --num 20
```

### Generate Data for Specific Models

```bash
python manage.py populate myapp --models Author Book --num 15
```

### Control ManyToMany Relationships

```bash
python manage.py populate myapp --num 10 --m2m 5
```

## Usage Examples

### Basic Example

```bash
# Generate 10 fake records for all models in the "books" app
python manage.py populate books --num 10
```

### Multiple Apps

```bash
# Generate fake data for multiple apps
python manage.py populate books authors publishers --num 25
```

### Specific Models

```bash
# Generate fake data only for Author and Book models
python manage.py populate books --models Author Book --num 50
```

### With ManyToMany Relations

```bash
# Generate 20 records with 5 related objects for each ManyToMany field
python manage.py populate books --num 20 --m2m 5
```

## Command Options

| Option | Description | Default |
|--------|-------------|---------|
| `apps` | App labels to fill with fake data | All apps |
| `--all` | Generate fake data for all models | False |
| `--models` | Specific model names to fill | All models in app |
| `--num` | Number of objects to generate | 1 |
| `--m2m` | Number of related objects for ManyToMany fields | 1 |

## Field Mapping

Django Fake Filler intelligently maps field names to appropriate Faker methods:

### Supported Field Name Patterns

- **Email**: `email`, `email_address`, `user_email`
- **Names**: `first_name`, `last_name`, `full_name`, `name`
- **Phone**: `phone`, `phone_number`, `mobile`
- **Address**: `address`, `street`, `city`, `country`, `zipcode`
- **Company**: `company`, `company_name`
- **URLs**: `url`, `website`, `domain`
- **Text**: `title`, `description`, `bio`, `summary`
- **Dates**: `date`, `birth_date`, `created_at`
- **And many more...**

### Field Type Mapping

The package also maps Django field types to appropriate fake data:

- `CharField` → Random text
- `EmailField` → Valid email addresses
- `IntegerField` → Random integers
- `DecimalField` → Random decimal numbers
- `DateField` → Random dates
- `DateTimeField` → Random datetime values
- `BooleanField` → Random boolean values
- `URLField` → Valid URLs
- `TextField` → Paragraphs of lorem ipsum
- `SlugField` → URL-safe slugs

## Configuration

You can customize the fake data generation by modifying `model_populator/field_mappings.py`:

### Control Related Object Creation

**The Smart Default** - Reuses existing related objects instead of creating duplicates:

```python
# In your Django settings.py
AUTO_CREATE_RELATED_MODELS = True  # Default behavior

# When generating 100 books:
# - Creates a few authors/publishers first
# - Reuses them across books (realistic!)
# - Result: 100 books share ~20 authors and ~15 publishers
```

This is what makes our data realistic - just like in the real world where Stephen King has written dozens of books, not one book per author!

### Exclude Apps or Models

```python
EXCLUDED_APPS = ['admin', 'contenttypes', 'auth', 'sessions']
EXCLUDED_MODELS = ['LogEntry', 'Permission']
```

### Custom Field Mappings

```python
FIELD_NAME_MAPPING = {
    'custom_field': 'faker_method',
    # Add your custom mappings
}
```

## Requirements

- Python >= 3.8
- Django >= 3.2
- Faker >= 37.0
- tqdm >= 4.67

## Use Cases

- **Development**: Quickly populate development databases with realistic test data
- **Testing**: Generate test fixtures for unit and integration tests
- **Demos**: Create convincing demo data for presentations
- **Prototyping**: Speed up prototyping with ready-made sample data

## How It Works

1. Scans your Django models and their fields
2. Matches field names and types to appropriate Faker methods
3. Handles foreign key relationships by creating related objects
4. Respects unique constraints and validation rules
5. Generates data with progress tracking

## Examples

### E-commerce Project

```bash
# Generate products, categories, and orders
python manage.py populate shop --models Category Product Order --num 100 --m2m 3
```

### Blog Application

```bash
# Generate authors, posts, and comments
python manage.py populate blog --num 50
```

### User Management

```bash
# Generate user profiles with related data
python manage.py populate accounts --models Profile --num 200
```

## Troubleshooting

### Unique Constraint Errors

The package handles unique fields automatically, but if you encounter issues:
- Reduce the `--num` parameter
- Check your model's unique constraints
- The package will skip records that violate unique constraints

### Foreign Key Issues

If related objects aren't being created:
- Ensure `AUTO_CREATE_RELATED_MODELS = True` in settings
- Check that related models aren't in `EXCLUDED_MODELS`

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on:

- Setting up the development environment
- Running tests
- Submitting pull requests
- Code style guidelines

> **💡 Fast Setup**: We recommend using [uv](https://github.com/astral-sh/uv) for 10-100x faster package installation. See our [uv Guide](UV_GUIDE.md) for details.

### Quick Start for Contributors

```bash
# Clone the repository
git clone https://github.com/YOUR_ORG/django_model_populator.git
cd django_model_populator

# Set up development environment (choose one):

# Option 1: Using uv (fastest - recommended)
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt

# Option 2: Using venv
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Run migrations and tests
python manage.py migrate
python manage.py test

# Try the example app
python manage.py populate books --num 10
```

See [TESTING.md](TESTING.md) for comprehensive testing documentation. Please feel free to submit a Pull Request.

## Credits & Acknowledgments

This project would not be possible without:

### [Faker](https://github.com/joke2k/faker)
The amazing Python library by **Daniele Faraglia** and contributors that powers all our fake data generation. Faker provides hundreds of data providers across multiple locales, making realistic test data generation a breeze.

- **Repository**: https://github.com/joke2k/faker
- **Documentation**: https://faker.readthedocs.io/
- **License**: MIT

**Thank you to the Faker team** for creating such a versatile and well-maintained library! 🎉

### Community
Thanks to all contributors who help improve this project and make Django development easier for everyone.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Mathias AG <mathiasag07@gmail.com>

## Links

- PyPI: https://pypi.org/project/django_model_populator/
- GitHub: https://github.com/mathiasag7/django_model_populator
- Issues: https://github.com/mathiasag7/django_model_populator/issues

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.
