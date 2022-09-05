from django.db import models
from django.db.models.functions import Concat
from django.db.models import Value


class BookQuerySet(models.QuerySet):
    def available(self):
        from .models import Book

        return self.filter(loan_status=Book.AVAILABLE)

    def lent(self):
        from .models import Book

        return self.filter(loan_status=Book.LENT)


class AuthorQuerySet(models.QuerySet):
    def search(self, query):
        return self.annotate(full_name=Concat("name", Value(" "), "last_name")).filter(
            full_name__icontains=query
        )
