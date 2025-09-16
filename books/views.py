from django.views import generic
from django.urls import reverse_lazy

from books.forms import BookForm
from books.models import Book


class BookListView(generic.ListView):
    model = Book
    template_name = "books/books_list_page.html"
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