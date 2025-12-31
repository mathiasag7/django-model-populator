from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    author = models.ForeignKey('Author', on_delete=models.CASCADE, related_name='books')
    publisher = models.ForeignKey('Publisher', on_delete=models.CASCADE, related_name='books')
    publication_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    pages = models.PositiveIntegerField()
    cover_image = models.URLField(blank=True, null=True)
    language = models.CharField(max_length=30, default='English')
    genre = models.CharField(max_length=50, blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        unique_together = ['title', 'isbn', 'publisher', 'author']


    def __str__(self):
        return self.title
    

class Author(models.Model):
    name = models.CharField(max_length=100, unique=True)
    bio = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'


    def __str__(self):
        return self.name
    

class Publisher(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    established_date = models.DateField(blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    logo = models.URLField(blank=True, null=True)
    social_media_links = models.JSONField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Publisher'
        verbose_name_plural = 'Publishers'


    def __str__(self):
        return self.name