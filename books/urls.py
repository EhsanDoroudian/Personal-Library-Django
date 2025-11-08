from django.urls import path
from books import views


app_name = "books"

urlpatterns = [
    path("", views.BookListView.as_view(), name="book-list"),
    path("me/", views.MyBookListView.as_view(), name="my-books"),
    path("<int:pk>/", views.BookDetailView.as_view(), name="book-detail"),
    path("create/", views.BookCreateView.as_view(), name="book-create"),
    path("<int:pk>/update/", views.BookUpdateView.as_view(), name="book-update"),
    path("<int:pk>/delete/", views.BookDeleteView.as_view(), name="book-delete"),
]