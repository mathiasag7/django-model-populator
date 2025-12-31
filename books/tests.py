from django.test import TestCase
from django.core.management import call_command
from io import StringIO
from books.models import Book, Author, Publisher


class BooksExampleAppTestCase(TestCase):
    """Test suite for the books example application"""

    def setUp(self):
        """Set up test fixtures"""
        Book.objects.all().delete()
        Author.objects.all().delete()
        Publisher.objects.all().delete()

        # Reset the global object counter
        from model_populator import engine

        engine._OBJECT_CREATED_COUNT.clear()

    def test_models_are_registered(self):
        """Test that all models are properly registered"""
        from django.apps import apps

        self.assertIsNotNone(apps.get_model("books", "Book"))
        self.assertIsNotNone(apps.get_model("books", "Author"))
        self.assertIsNotNone(apps.get_model("books", "Publisher"))

    def test_author_creation(self):
        """Test manual author creation"""
        author = Author.objects.create(name="J.K. Rowling", email="jk@example.com", bio="British author")
        self.assertEqual(Author.objects.count(), 1)
        self.assertEqual(author.name, "J.K. Rowling")

    def test_publisher_creation(self):
        """Test manual publisher creation"""
        publisher = Publisher.objects.create(name="Penguin Books", contact_email="info@penguin.com", is_active=True)
        self.assertEqual(Publisher.objects.count(), 1)
        self.assertTrue(publisher.is_active)

    def test_book_with_relationships(self):
        """Test creating a book with author and publisher relationships"""
        author = Author.objects.create(name="George Orwell")
        publisher = Publisher.objects.create(name="Secker and Warburg")

        book = Book.objects.create(
            title="1984",
            description="Dystopian novel",
            author=author,
            publisher=publisher,
            publication_date="1949-06-08",
            isbn="9780451524935",
            pages=328,
            price=15.99,
        )

        self.assertEqual(book.author, author)
        self.assertEqual(book.publisher, publisher)
        self.assertEqual(author.books.count(), 1)

    def test_book_string_representation(self):
        """Test __str__ method of Book model"""
        author = Author.objects.create(name="Test Author")
        publisher = Publisher.objects.create(name="Test Publisher")

        book = Book.objects.create(
            title="Test Book",
            description="Test description",
            author=author,
            publisher=publisher,
            publication_date="2024-01-01",
            isbn="1234567890123",
            pages=200,
            price=10.00,
        )

        self.assertEqual(str(book), "Test Book")

    def test_author_string_representation(self):
        """Test __str__ method of Author model"""
        author = Author.objects.create(name="Test Author")
        self.assertEqual(str(author), "Test Author")

    def test_publisher_string_representation(self):
        """Test __str__ method of Publisher model"""
        publisher = Publisher.objects.create(name="Test Publisher")
        self.assertEqual(str(publisher), "Test Publisher")

    def test_unique_isbn_constraint(self):
        """Test that ISBN must be unique"""
        author = Author.objects.create(name="Test Author")
        publisher = Publisher.objects.create(name="Test Publisher")

        Book.objects.create(
            title="Book 1",
            description="Description 1",
            author=author,
            publisher=publisher,
            publication_date="2024-01-01",
            isbn="1234567890123",
            pages=200,
            price=10.00,
        )

        # Attempting to create another book with the same ISBN should fail
        with self.assertRaises(Exception):
            Book.objects.create(
                title="Book 2",
                description="Description 2",
                author=author,
                publisher=publisher,
                publication_date="2024-01-02",
                isbn="1234567890123",  # Same ISBN
                pages=250,
                price=12.00,
            )

    def test_unique_author_name_constraint(self):
        """Test that author names must be unique"""
        Author.objects.create(name="John Doe")

        with self.assertRaises(Exception):
            Author.objects.create(name="John Doe")

    def test_cascade_delete(self):
        """Test that deleting an author cascades to books"""
        author = Author.objects.create(name="Test Author")
        publisher = Publisher.objects.create(name="Test Publisher")

        Book.objects.create(
            title="Book 1",
            description="Description",
            author=author,
            publisher=publisher,
            publication_date="2024-01-01",
            isbn="1234567890123",
            pages=200,
            price=10.00,
        )

        self.assertEqual(Book.objects.count(), 1)
        author.delete()
        self.assertEqual(Book.objects.count(), 0)


class PopulateManagementCommandTestCase(TestCase):
    """Test suite for the populate management command"""

    def setUp(self):
        """Clean up before each test"""
        Book.objects.all().delete()
        Author.objects.all().delete()
        Publisher.objects.all().delete()

        # Reset the global object counter
        from model_populator import engine

        engine._OBJECT_CREATED_COUNT.clear()

    def test_populate_command_books_app(self):
        """Test the populate command for books app"""
        out = StringIO()
        call_command("populate", "books", "--num", "5", stdout=out)

        # Should create authors, publishers, and books
        self.assertGreater(Author.objects.count(), 0)
        self.assertGreater(Publisher.objects.count(), 0)
        self.assertGreater(Book.objects.count(), 0)

    def test_populate_command_specific_model(self):
        """Test the populate command for specific model"""
        out = StringIO()
        call_command("populate", "books", "--models", "Author", "--num", "10", stdout=out)

        # Should have created at least some authors
        self.assertGreater(Author.objects.count(), 0)

    def test_populate_command_multiple_models(self):
        """Test the populate command for multiple specific models"""
        out = StringIO()
        call_command("populate", "books", "--models", "Author", "Publisher", "--num", "5", stdout=out)

        # Should have created some of each model
        self.assertGreater(Author.objects.count(), 0)
        self.assertGreater(Publisher.objects.count(), 0)
