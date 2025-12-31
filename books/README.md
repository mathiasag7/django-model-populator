# Books Example App

This is a complete Django app demonstrating how to use the Django Model Populator package.

## Purpose

This example app serves multiple purposes:

1. **Documentation by Example**: Shows real-world usage patterns
2. **Testing**: Provides models for testing the populator functionality
3. **Contribution Validation**: Contributors can use this to test their changes
4. **Reference Implementation**: Best practices for Django model design

## Models

### Author

Represents a book author with biographical information.

**Fields:**
- `name` (CharField, unique): Author's full name
- `bio` (TextField, optional): Biographical information
- `email` (EmailField, optional): Contact email
- `website` (URLField, optional): Personal or professional website
- `birth_date` (DateField, optional): Date of birth
- `created_at` (DateTimeField, auto): Record creation timestamp
- `updated_at` (DateTimeField, auto): Last update timestamp

**Relationships:**
- One-to-Many with Book (an author can write multiple books)

**Example:**
```python
from books.models import Author

author = Author.objects.create(
    name="Isaac Asimov",
    email="isaac@example.com",
    bio="Prolific science fiction author",
    birth_date="1920-01-02"
)
```

### Publisher

Represents a publishing company.

**Fields:**
- `name` (CharField, unique): Publisher name
- `address` (TextField, optional): Physical address
- `website` (URLField, optional): Company website
- `established_date` (DateField, optional): Date company was founded
- `contact_email` (EmailField, optional): General contact email
- `phone_number` (CharField, optional): Contact phone
- `description` (TextField, optional): Company description
- `logo` (URLField, optional): Logo image URL
- `social_media_links` (JSONField, optional): Social media profiles
- `is_active` (BooleanField): Whether publisher is currently active
- `created_at` (DateTimeField, auto): Record creation timestamp
- `updated_at` (DateTimeField, auto): Last update timestamp

**Relationships:**
- One-to-Many with Book (a publisher publishes multiple books)

**Example:**
```python
from books.models import Publisher

publisher = Publisher.objects.create(
    name="Penguin Random House",
    website="https://www.penguinrandomhouse.com",
    is_active=True,
    social_media_links={
        "twitter": "@penguinrandom",
        "facebook": "penguinrandomhouse"
    }
)
```

### Book

Represents a published book.

**Fields:**
- `title` (CharField): Book title
- `description` (TextField): Book description/summary
- `author` (ForeignKey to Author): Book's author
- `publisher` (ForeignKey to Publisher): Book's publisher
- `publication_date` (DateField): When the book was published
- `isbn` (CharField, unique): International Standard Book Number
- `pages` (PositiveIntegerField): Number of pages
- `cover_image` (URLField, optional): Cover image URL
- `language` (CharField): Language of the book (default: English)
- `genre` (CharField, optional): Book genre
- `summary` (TextField, optional): Detailed summary
- `price` (DecimalField): Book price
- `created_at` (DateTimeField, auto): Record creation timestamp
- `updated_at` (DateTimeField, auto): Last update timestamp

**Constraints:**
- `unique_together`: ['title', 'isbn', 'publisher', 'author']
- `ordering`: ['-created_at'] (newest first)

**Relationships:**
- Many-to-One with Author (many books can have one author)
- Many-to-One with Publisher (many books can have one publisher)

**Example:**
```python
from books.models import Book, Author, Publisher

author = Author.objects.get(name="Isaac Asimov")
publisher = Publisher.objects.get(name="Penguin Random House")

book = Book.objects.create(
    title="Foundation",
    description="First book in the Foundation series",
    author=author,
    publisher=publisher,
    publication_date="1951-05-01",
    isbn="9780553293357",
    pages=255,
    price=12.99,
    genre="Science Fiction"
)
```

## Using with Model Populator

### Generate Fake Data

```bash
# Generate 10 of each model in the books app
python manage.py populate books --num 10

# Generate only authors
python manage.py populate books --models Author --num 20

# Generate books (will automatically create authors and publishers)
python manage.py populate books --models Book --num 15
```

### Programmatic Usage

```python
from model_populator.engine import generate_fake_data
from books.models import Author, Publisher, Book

# Generate 5 authors
generate_fake_data(Author, num_objects=5)

# Generate 3 publishers
generate_fake_data(Publisher, num_objects=3)

# Generate 10 books (will use existing authors/publishers)
generate_fake_data(Book, num_objects=10)
```

## Field Type Coverage

This example app demonstrates the populator's ability to handle:

### Basic Field Types
- ✅ CharField (with and without max_length)
- ✅ TextField
- ✅ EmailField
- ✅ URLField
- ✅ DateField
- ✅ DateTimeField (auto_now, auto_now_add)
- ✅ BooleanField
- ✅ PositiveIntegerField
- ✅ DecimalField
- ✅ JSONField

### Constraints
- ✅ Unique fields (name, isbn)
- ✅ Unique together constraints
- ✅ Blank/null handling
- ✅ Default values

### Relationships
- ✅ ForeignKey (with cascade delete)
- ✅ Related names (reverse relationships)
- ✅ Automatic related object creation

### Field Name Recognition
The populator intelligently recognizes field names:
- `email` → generates valid emails
- `phone_number` → generates phone numbers
- `website` → generates URLs
- `address` → generates addresses
- `description`/`bio`/`summary` → generates text
- `name`/`title` → generates short text

## Admin Interface

All models are registered in the Django admin:

```python
# books/admin.py
from django.contrib import admin
from .models import Book, Author, Publisher

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Publisher)
```

Access at: http://127.0.0.1:8000/admin/

## Running Tests

The books app includes comprehensive tests:

```bash
# Run all books tests
python manage.py test books

# Run specific test class
python manage.py test books.tests.BooksExampleAppTestCase

# Run with verbose output
python manage.py test books --verbosity=2
```

## Testing Your Changes

If you're contributing to the project:

1. **Make your changes** to the populator engine
2. **Run the example app**:
   ```bash
   python manage.py migrate
   python manage.py populate books --num 10
   ```
3. **Verify in shell**:
   ```bash
   python manage.py shell
   >>> from books.models import Book
   >>> Book.objects.all()
   ```
4. **Run tests**:
   ```bash
   python manage.py test
   ```

## Common Scenarios

### Scenario 1: Test ForeignKey Handling

```python
from model_populator.engine import generate_fake_data
from books.models import Book

# Generate books - should auto-create authors and publishers
generate_fake_data(Book, num_objects=5)

# Verify relationships
for book in Book.objects.all():
    print(f"{book.title} by {book.author.name}")
    print(f"Published by {book.publisher.name}")
```

### Scenario 2: Test Unique Constraints

```python
from model_populator.engine import generate_fake_data
from books.models import Author

# Generate many authors - all should have unique names
generate_fake_data(Author, num_objects=50)

# Verify uniqueness
names = Author.objects.values_list('name', flat=True)
print(f"Total authors: {len(names)}")
print(f"Unique names: {len(set(names))}")
assert len(names) == len(set(names))
```

### Scenario 3: Test Complex Fields

```python
from model_populator.engine import generate_fake_data
from books.models import Publisher

# Generate publishers with JSON fields
generate_fake_data(Publisher, num_objects=5)

# Check JSON field population
for pub in Publisher.objects.all():
    print(f"{pub.name}: {pub.social_media_links}")
```

## Extending the Example

Want to add more models? Follow this pattern:

```python
# books/models.py

class Review(models.Model):
    """Book review"""
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    reviewer_name = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField()  # 1-5 stars
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['book', 'reviewer_name']
```

Then test it:

```python
from model_populator.engine import generate_fake_data
from books.models import Review

generate_fake_data(Review, num_objects=20)
```

## Troubleshooting

### Issue: Unique constraint violations

**Solution**: The populator uses `SafeUniqueProxy` to handle this, but if you generate many objects:
- Reduce the number of objects
- Increase the pool of potential unique values
- Check field mappings in `model_populator/field_mappings.py`

### Issue: Related objects not created

**Solution**: Check `AUTO_CREATE_RELATED_MODELS` setting:
```python
# settings.py
AUTO_CREATE_RELATED_MODELS = True  # Default
```

### Issue: Fields not populating correctly

**Solution**: Check field name patterns in `FIELD_NAME_MAPPING`:
```python
# model_populator/field_mappings.py
FIELD_NAME_MAPPING = {
    "email": ["email", "e_mail"],
    "phone_number": ["phone", "phone_number", "mobile"],
    # Add your custom patterns
}
```

## Contributing

When adding features, use this example app to:
1. Test your changes manually
2. Write automated tests in `books/tests.py`
3. Document new field types or patterns
4. Verify edge cases

See [TESTING.md](../TESTING.md) for detailed testing guidelines.
