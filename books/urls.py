from django.urls import path

from .views import AuthorDetailView, BookListView, BookDetailView

urlpatterns = [
    path('', BookListView.as_view(), name='book-list'),
    path('<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('author/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),
]
