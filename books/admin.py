from django.contrib import admin

from books.models import Book, Category


class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "author"]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["title"]

admin.site.register(Book, BookAdmin)
admin.site.register(Category, CategoryAdmin)