# -*- coding: utf-8 -*-
from django.contrib import admin

from django.utils.translation import gettext_lazy as _

from .models import Author, Book, Genre, Publisher


class AuthorAdmin(admin.ModelAdmin):
    pass


class BookAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'author','publisher','genre',)
        }),
        ('Classificazione', {
            'fields': ('column','palco','number',)
        }),
        ('Loan', {
            'fields': ('loan_status',)
        }),            
    )

    
    list_display = ('title','column','palco','number','genre','loan_status')
    search_fields = ['title']     
    list_filter = ('genre','loan_status',)
    filter_horizontal = ('author',)

class PublisherAdmin(admin.ModelAdmin):
    pass

class GenreAdmin(admin.ModelAdmin):
    pass

admin.site.register(Book, BookAdmin)
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre, GenreAdmin)