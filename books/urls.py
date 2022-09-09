from django.urls import path

from .views import (
    AuthorDetailView,
    AuthorsAutocomplete,
    BookListView,
    BookDetailView,
    LoanCreateView,
    return_book, export_books_to_csv_view, BooksStampsView
)

app_name = "books"

urlpatterns = [
    path("", BookListView.as_view(), name="book-list"),
    path("<int:pk>/", BookDetailView.as_view(), name="book-detail"),
    path("author/<int:pk>/", AuthorDetailView.as_view(), name="author-detail"),
    path("authors", AuthorsAutocomplete.as_view(), name="author-live-search"),
    path("<int:book_id>/borrow/",
         LoanCreateView.as_view(), name="loan-create-view"),
    path("<int:book_id>/return-book/", return_book, name="return-book"),
    path("export-to-csv", export_books_to_csv_view, name="export-to-csv"),
    path("books-stamps", BooksStampsView.as_view(), name="books-stamps"),
]
