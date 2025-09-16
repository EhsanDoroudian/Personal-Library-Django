from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name="title")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Categories"


class Book(models.Model):
    # TODO : check all potential blank or null fields and check comments
    Book_STATU_READ = "R"
    BOOK_STATUS_NOT_READ = "NR"
    BOOK_STATUS_BORROWED = "B"

    isbn13_digits_only = RegexValidator(
        regex=r'^(978|979)\d{10}$',
        message='Enter a valid ISBN-13 (13 digits starting with 978 or 979)'
    )

    STATUS_CHOICES = [
        (Book_STATU_READ, "Read"),
        (BOOK_STATUS_NOT_READ, "Not Read"),
        (BOOK_STATUS_BORROWED, "Borrowed")
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="books")
    title = models.CharField(max_length=50, verbose_name="title")
    description = models.TextField(verbose_name="description")
    author = models.CharField(max_length=50, verbose_name="author")
    translator = models.CharField(max_length=50, blank=True, verbose_name="translator")
    publisher = models.CharField(max_length=50, blank=True, verbose_name="publisher")
    price = models.PositiveIntegerField(verbose_name="price", blank=True, null=True)
    year = models.PositiveIntegerField(verbose_name="year", blank=True, null=True)
    shabak_number = models.CharField(
                                unique=True,
                                max_length=13,
                                blank=True,
                                verbose_name="ISBN-13",
                                validators=[isbn13_digits_only],
                                help_text="Enter ISBN-13 (13 digits starting with 978 or 979)"
                                )
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="books")
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default=Book_STATU_READ)
    page_number = models.PositiveIntegerField(verbose_name="Number of page", null=True, blank=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)
    # cover = models.ImageField(upload_to=*)

    def __str__(self):
        return f"{self.title} by {self.author}"
    
    def get_absolute_url(self):
        return reverse("books:book-detail", kwargs={"pk": self.id})
    
    class Meta:
        ordering = ['-created_datetime']
