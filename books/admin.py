from django.contrib import admin
from .models import Category, Book
from django.db.models import Count

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'book_count')  # Added book_count to list_display for visibility
    search_fields = ('title',)
    ordering = ('title',)
    list_per_page = 20

    def get_queryset(self, request):
        # Prefetch related books to avoid N+1 queries for book_count and any book displays
        return super().get_queryset(request).prefetch_related('books').annotate(books_count=Count('books'))

    def book_count(self, category):
        # Efficient count using prefetched data (no extra query)
        return category.books_count

    book_count.short_description = 'Number of Books '


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'get_category_title',  # Custom method to display category title (uses select_related)
        'status',
        'year',
        'price',
        'created_datetime',
    )
    list_filter = (
        'status',
        'category',
        'year',
    )
    search_fields = (
        'title',
        'author',
        'shabak_number',
        'publisher',
        'translator',
    )
    list_select_related = ['category']
    list_editable = ('status',)
    list_per_page = 20
    date_hierarchy = 'created_datetime'
    ordering = ('-created_datetime',)
    raw_id_fields = ('user',)  # Reduces queries for user FK widget
    autocomplete_fields = ('category',)  # Efficient category selection with select_related
    readonly_fields = ('created_datetime', 'modified_datetime')
    fieldsets = (
        ('Book Information', {
            'fields': (
                'title',
                'author',
                'translator',
                'publisher',
                'description',
                'shabak_number',
                'category'
            )
        }),
        ('Details', {
            'fields': (
                'price',
                'year',
                'page_number',
                'status'
            ),
            'classes': ('collapse',)  # Optional: Collapsible for better UX
        }),
        ('Metadata', {
            'fields': (
                'user',
                'created_datetime',
                'modified_datetime'
            ),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        # select_related for FKs (category, user) to avoid N+1 queries when displaying lists
        # This directly addresses duplicated category queries
        return super().get_queryset(request).select_related('category', 'user')

    def get_category_title(self, book):
        # Custom display for category to ensure it uses the prefetched/selected data
        return book.category.title if book.category else '-'
    get_category_title.short_description = 'Category'
    get_category_title.admin_order_field = 'category__title'  # Allows sorting by category title

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        # Avoid DISTINCT for performance in searches
        return queryset, False