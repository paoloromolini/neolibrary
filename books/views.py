from django.views.generic.list import ListView
from django.views.generic.detail import  DetailView
from django.views.generic.edit import CreateView
from .models import Author, Book, Genre, Loan
from .forms import SearchBooksForm
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q

from simple_search import search_filter


class CurrentSiteMixin(object):
    """ return the current site """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site'] = get_current_site(self.request)
        return context


class BookListView(CurrentSiteMixin, ListView):

    model = Book
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchBooksForm()
        queries = self.request.GET.copy()
        if 'page' in queries:
            del queries['page']
        context['search'] = queries
        context['genres'] = Genre.objects.all()
        return context

    def get_queryset(self):
        """
        The main search
        """
        result =  Book.objects.none()
        author_q = self.request.GET.get("author")
        title_q = self.request.GET.get("title")
        column_q = self.request.GET.get("column")
        palco_q = self.request.GET.get("palco")
        number_q = self.request.GET.get("number")
        genre_q = self.request.GET.get("genre")
        if any((author_q, title_q, column_q, palco_q, number_q, genre_q)):
            result = Book.objects.all()
            if title_q:
                search_fields = ['title']
                f = search_filter(search_fields, title_q)
                result = result.filter(f)    
            if author_q:
                authors = Author.objects.search(author_q)
                result = result.filter(author__in=authors.values_list('pk', flat=True))
            if column_q:
                result = result.filter(column__iexact=column_q.strip())
            if palco_q:
                result = result.filter(palco__iexact=palco_q.strip())
            if number_q:
                result = result.filter(number__iexact=number_q.strip())
            if genre_q:
                result = result.filter(genre__code=genre_q)
        return result

class BookDetailView(CurrentSiteMixin, DetailView):

    model = Book


class AuthorDetailView(CurrentSiteMixin, DetailView):

    model = Author


class AuthorsAutocomplete(ListView):

    model = Author

    def get_queryset(self):
        query = self.request.GET.get('q')
        authors = Author.objects.none()
        if query and len(query) > 1:
            authors = Author.objects.search(query)
        return authors


class LoanCreateView(CurrentSiteMixin, CreateView):

    model  = Loan
    fields = ['loan_holder']
    success_url = '../'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.kwargs)
        context['book'] = 1
        return context

    def form_valid(self, form):
        book = Book.objects.get(pk=self.kwargs['book_id'])
        form.instance.book = book
        book.loan_status = Book.LENT
        book.save()
        return super().form_valid(form)