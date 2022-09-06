from django.urls import path

from .views import (
    AuthorDetailView,
    AuthorsAutocomplete,
    BookListView,
    BookDetailView,
    LoanCreateView,
    return_book,
)

app_name = "books"

urlpatterns = [
    path("", BookListView.as_view(), name="book-list"),
    path("<int:pk>/", BookDetailView.as_view(), name="book-detail"),
    path("author/<int:pk>/", AuthorDetailView.as_view(), name="author-detail"),
    path("authors", AuthorsAutocomplete.as_view(), name="author-live-search"),
    path("<int:book_id>/borrow/", LoanCreateView.as_view(), name="loan-create-view"),
    path("<int:book_id>/return-book/", return_book, name="return-book"),
]
