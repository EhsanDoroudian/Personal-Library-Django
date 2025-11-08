from django.contrib.auth import get_user_model
from django.views import generic
from django.urls import reverse_lazy
from django.db.models import Count
from django.db.models import Q


from books.forms import BookForm
from books.models import Book, Category


class BookListView(generic.ListView):
    model = Book
    template_name = "books/books_list_page.html"
    context_object_name = "books"
    paginate_by = 12

    def get_queryset(self):
        queryset = Book.objects.all().select_related('user', 'category').order_by('-created_datetime')
        
        # Basic filters
        category_id = self.request.GET.get('category')        
        status = self.request.GET.get('status')
        search = self.request.GET.get('search')
        
        # Advanced filters
        author = self.request.GET.get('author')
        publisher = self.request.GET.get('publisher')
        year_from = self.request.GET.get('year_from')
        year_to = self.request.GET.get('year_to')
        pages_min = self.request.GET.get('pages_min')
        pages_max = self.request.GET.get('pages_max')
        
        # Apply basic filters
        if category_id and category_id.isdigit():
            queryset = queryset.filter(category_id=int(category_id))
        if status:
            queryset = queryset.filter(status=status)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(author__icontains=search) |
                Q(description__icontains=search)
            )
            
        # Apply advanced filters
        if author:
            queryset = queryset.filter(author__icontains=author)
        if publisher:
            queryset = queryset.filter(publisher__icontains=publisher)
        if year_from:
            queryset = queryset.filter(year__gte=year_from)
        if year_to:
            queryset = queryset.filter(year__lte=year_to)
        if pages_min:
            queryset = queryset.filter(page_number__gte=pages_min)
        if pages_max:
            queryset = queryset.filter(page_number__lte=pages_max)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        User = get_user_model()
        
        # Statistics
        books_number = Book.objects.aggregate(book_num=Count("id"))
        users_number = User.objects.aggregate(user_num=Count("id"))
        
        context["books_number"] = books_number['book_num']
        context["users_number"] = users_number['user_num']
        context["categories"] = Category.objects.all()
        
        # Current filter values
        context["current_category"] = self.request.GET.get('category', '')
        context["current_status"] = self.request.GET.get('status', '')
        context["current_search"] = self.request.GET.get('search', '')
        
        # Advanced filter values
        context["current_author"] = self.request.GET.get('author', '')
        context["current_publisher"] = self.request.GET.get('publisher', '')
        context["current_year_from"] = self.request.GET.get('year_from', '')
        context["current_year_to"] = self.request.GET.get('year_to', '')
        context["current_pages_min"] = self.request.GET.get('pages_min', '')
        context["current_pages_max"] = self.request.GET.get('pages_max', '')
        
        # Get unique values for dropdowns
        context["all_authors"] = Book.objects.values_list('author', flat=True).distinct().order_by('author')
        context["all_publishers"] = Book.objects.values_list('publisher', flat=True).distinct().order_by('publisher')
        context["all_years"] = Book.objects.exclude(year__isnull=True).values_list('year', flat=True).distinct().order_by('-year')
        
        context["current_category_obj"] = None
        if current_category := self.request.GET.get('category'):
            try:
             context["current_category_obj"] = Category.objects.get(id=int(current_category))
            except (ValueError, Category.DoesNotExist):
                pass
        return context
class MyBookListView(generic.ListView):
    model = Book
    template_name = "books/my_books_page.html"
    context_object_name = "books"


class BookDetailView(generic.DetailView):
    model = Book
    template_name = "books/book_detail_page.html"
    context_object_name = "book"


class BookCreateView(generic.CreateView):
    model = Book
    form_class = BookForm
    template_name = "books/book_create_page.html"

    def form_invalid(self, form):
        print(form.errors)  # Debug: Print form errors to console
        return super().form_invalid(form)
    
 
class BookUpdateView(generic.UpdateView):
    model = Book
    form_class = BookForm
    template_name = "books/book_update_page.html"


class BookDeleteView(generic.DeleteView):
    model = Book
    template_name = "books/book_delete_page.html"
    success_url = reverse_lazy("books:book-list")