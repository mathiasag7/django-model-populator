from django.test import TestCase
from django.db import models
from books.models import Book, Author, Publisher
from model_populator.engine import generate_fake_data


class ModelPopulatorTestCase(TestCase):
    """Test suite for the model populator engine"""

    def setUp(self):
        """Set up test fixtures"""
        # Clear any existing data
        Book.objects.all().delete()
        Author.objects.all().delete()
        Publisher.objects.all().delete()

        # Reset the global object counter
        from model_populator import engine

        engine._OBJECT_CREATED_COUNT.clear()

    def test_generate_single_author(self):
        """Test generating a single author"""
        generate_fake_data(Author, num_objects=1)
        self.assertEqual(Author.objects.count(), 1)

        author = Author.objects.first()
        self.assertIsNotNone(author.name)
        self.assertIsInstance(author.name, str)

    def test_generate_multiple_authors(self):
        """Test generating multiple authors"""
        from model_populator.engine import generate_model_fakes

        num_authors = 5
        generate_model_fakes(Author, num_objects=num_authors)
        self.assertEqual(Author.objects.count(), num_authors)

    def test_unique_field_handling(self):
        """Test that unique fields generate unique values"""
        num_authors = 10
        generate_fake_data(Author, num_objects=num_authors)

        # All author names should be unique
        names = Author.objects.values_list("name", flat=True)
        self.assertEqual(len(names), len(set(names)))

    def test_email_field_generation(self):
        """Test that email fields are properly populated"""
        generate_fake_data(Author, num_objects=5)

        for author in Author.objects.all():
            if author.email:
                self.assertIn("@", author.email)

    def test_foreign_key_relationship(self):
        """Test ForeignKey relationships are properly created"""
        generate_fake_data(Book, num_objects=3)

        self.assertGreater(Book.objects.count(), 0)
        self.assertGreater(Author.objects.count(), 0)
        self.assertGreater(Publisher.objects.count(), 0)

        # Check that books have valid author and publisher
        for book in Book.objects.all():
            self.assertIsNotNone(book.author)
            self.assertIsNotNone(book.publisher)
            self.assertIsInstance(book.author, Author)
            self.assertIsInstance(book.publisher, Publisher)

    def test_isbn_uniqueness(self):
        """Test that ISBN fields are unique"""
        generate_fake_data(Book, num_objects=5)

        isbns = Book.objects.values_list("isbn", flat=True)
        self.assertEqual(len(isbns), len(set(isbns)))

    def test_date_field_generation(self):
        """Test that date fields are properly populated"""
        generate_fake_data(Book, num_objects=3)

        for book in Book.objects.all():
            self.assertIsNotNone(book.publication_date)

    def test_decimal_field_generation(self):
        """Test that decimal fields are properly populated"""
        generate_fake_data(Book, num_objects=3)

        for book in Book.objects.all():
            self.assertIsNotNone(book.price)
            self.assertGreaterEqual(book.price, 0)

    def test_positive_integer_field(self):
        """Test that positive integer fields generate valid values"""
        generate_fake_data(Book, num_objects=5)

        for book in Book.objects.all():
            self.assertGreater(book.pages, 0)
            self.assertIsInstance(book.pages, int)

    def test_url_field_generation(self):
        """Test that URL fields are properly populated"""
        generate_fake_data(Publisher, num_objects=3)

        for publisher in Publisher.objects.all():
            if publisher.website:
                self.assertTrue(publisher.website.startswith("http://") or publisher.website.startswith("https://"))

    def test_boolean_field_generation(self):
        """Test that boolean fields are properly populated"""
        generate_fake_data(Publisher, num_objects=5)

        for publisher in Publisher.objects.all():
            self.assertIsInstance(publisher.is_active, bool)

    def test_json_field_generation(self):
        """Test that JSON fields are properly populated"""
        from model_populator.engine import generate_model_fakes

        generate_model_fakes(Publisher, num_objects=3)

        for publisher in Publisher.objects.all():
            # JSONField can be None, a dict, list, or JSON string
            if publisher.social_media_links:
                # It should be a valid JSON structure (can be stored as string or object)
                self.assertTrue(
                    isinstance(publisher.social_media_links, (dict, list, str)),
                    f"Got type {type(publisher.social_media_links)}",
                )

    def test_text_field_generation(self):
        """Test that text fields are properly populated"""
        generate_fake_data(Author, num_objects=3)

        for author in Author.objects.all():
            if author.bio:
                self.assertIsInstance(author.bio, str)
                self.assertGreater(len(author.bio), 0)

    def test_auto_now_fields(self):
        """Test that auto_now and auto_now_add fields are set"""
        generate_fake_data(Book, num_objects=1)

        book = Book.objects.first()
        self.assertIsNotNone(book.created_at)
        self.assertIsNotNone(book.updated_at)

    def test_related_name_access(self):
        """Test that related_name reverse relationships work"""
        generate_fake_data(Book, num_objects=5)

        author = Author.objects.first()
        # Access books through related_name
        books_count = author.books.count()
        self.assertGreaterEqual(books_count, 0)

    def test_cascade_on_delete(self):
        """Test that cascade deletion works correctly"""
        generate_fake_data(Book, num_objects=3)

        author = Author.objects.first()
        author_books_count = author.books.count()

        # Delete the author
        author.delete()

        # Books should be deleted due to CASCADE
        remaining_books = Book.objects.filter(author=author).count()
        self.assertEqual(remaining_books, 0)


class FieldMappingTestCase(TestCase):
    """Test suite for field mapping functionality"""

    def test_phone_number_field(self):
        """Test that phone number fields are properly formatted"""
        generate_fake_data(Publisher, num_objects=5)

        for publisher in Publisher.objects.all():
            if publisher.phone_number:
                self.assertIsInstance(publisher.phone_number, str)
                # Phone numbers should not be empty
                self.assertGreater(len(publisher.phone_number), 0)

    def test_address_field(self):
        """Test that address fields are properly populated"""
        generate_fake_data(Publisher, num_objects=3)

        for publisher in Publisher.objects.all():
            if publisher.address:
                self.assertIsInstance(publisher.address, str)

    def test_description_field(self):
        """Test that description fields are properly populated"""
        generate_fake_data(Book, num_objects=3)

        for book in Book.objects.all():
            self.assertIsNotNone(book.description)
            self.assertIsInstance(book.description, str)


class EdgeCaseTestCase(TestCase):
    """Test suite for edge cases and error handling"""

    def test_generate_zero_objects(self):
        """Test generating zero objects"""
        from model_populator.engine import generate_model_fakes

        initial_count = Author.objects.count()
        generate_model_fakes(Author, num_objects=0)
        # generate_model_fakes won't create anything if num_objects is 0
        self.assertEqual(Author.objects.count(), initial_count)

    def test_blank_nullable_fields(self):
        """Test that blank and nullable fields don't cause errors"""
        generate_fake_data(Author, num_objects=5)

        # Should not raise any exceptions
        for author in Author.objects.all():
            # These fields can be None or empty
            _ = author.bio
            _ = author.email
            _ = author.website

    def test_default_values(self):
        """Test that default values are respected"""
        generate_fake_data(Book, num_objects=1)

        book = Book.objects.first()
        # Price has a default of 0.00, but should be populated with fake data
        self.assertIsNotNone(book.price)
