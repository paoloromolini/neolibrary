from django.views.generic.list import ListView
from django.views.generic.detail import  DetailView
from .models import Author, Book
from django.contrib.sites.shortcuts import get_current_site



class CurrentSiteMixin(object):
    """ return the current site """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site'] = get_current_site(self.request)
        return context


class BookListView(CurrentSiteMixin, ListView):

    model = Book
    paginate_by = 50


class BookDetailView(CurrentSiteMixin, DetailView):

    model = Book


class AuthorDetailView(CurrentSiteMixin, DetailView):

    model = Author

