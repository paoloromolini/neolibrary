import csv
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import StreamingHttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from simple_search import search_filter

from .forms import SearchBooksForm
from .models import Author, Book, Genre, Loan


class CurrentSiteMixin(object):
    """return the current site"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["site"] = get_current_site(self.request)
        context["site_root"] = settings.SITE_ROOT
        return context


class BookListView(CurrentSiteMixin, ListView):

    model = Book
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SearchBooksForm()
        queries = self.request.GET.copy()
        if "page" in queries:
            del queries["page"]
        context["search"] = queries
        context["genres"] = Genre.objects.all()
        return context

    def get_queryset(self):
        """
        The main search
        """
        result = Book.objects.none()
        author_q = self.request.GET.get("author")
        title_q = self.request.GET.get("title")
        column_q = self.request.GET.get("column")
        palco_q = self.request.GET.get("palco")
        number_q = self.request.GET.get("number")
        genre_q = self.request.GET.get("genre")
        if any((author_q, title_q, column_q, palco_q, number_q, genre_q)):
            result = Book.objects.all()
            if title_q:
                search_fields = ["title"]
                f = search_filter(search_fields, title_q)
                result = result.filter(f)
            if author_q:
                authors = Author.objects.search(author_q)
                result = result.filter(author__in=authors.values_list("pk", flat=True))
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
        query = self.request.GET.get("q")
        authors = Author.objects.none()
        if query and len(query) > 1:
            authors = Author.objects.search(query)
        return authors


class LoanCreateView(CurrentSiteMixin, CreateView):

    model = Loan
    fields = ["loan_holder"]
    success_url = "../"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["book"] = 1
        return context

    def form_valid(self, form):
        book = Book.objects.get(pk=self.kwargs["book_id"])
        form.instance.book = book
        book.loan_status = Book.LENT
        book.save()
        return super().form_valid(form)


def return_book(request, book_id):
    book = get_object_or_404(Book, id=book_id, loan_status=Book.LENT)
    book.loan_status = Book.AVAILABLE
    book.save(update_fields=["loan_status"])
    return HttpResponseRedirect(book.get_absolute_url())


class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


def export_books_to_csv_view(request):
    """A view that streams a large CSV file."""
    # Generate a sequence of rows. The range is based on the maximum number of
    # rows that can be handled by a single sheet in most spreadsheet
    # applications.
    rows = ([
        str(book),
        ",".join([str(author) for author in book.author.all()]),
        str(book.publisher),
        str(book.genre),
        book.year_edition
    ] for book in Book.objects.all().order_by("author", "genre"))
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    return StreamingHttpResponse(
        (writer.writerow(row) for row in rows),
        content_type="text/csv",
        headers={
            f'Content-Disposition': 'attachment; filename="books.csv"'},
    )


class BooksStampsDashboard(CurrentSiteMixin, TemplateView):
    template_name = "books/book_stamp_dashboard.html"
    model = Book


class BooksStampsView(CurrentSiteMixin, ListView):
    template_name = "books/book_stamp.html"
    model = Book
    paginate_by = None


class BooksStampsSideView(CurrentSiteMixin, ListView):
    template_name = "books/book_stamp_side.html"
    model = Book
    paginate_by = None
