# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals


from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Author(models.Model):
    name = models.CharField(verbose_name=_('name'), max_length=100)
    last_name = models.CharField(verbose_name=_('last name'), max_length=100)

    def __str__(self):
        return '{} {}'.format(self.name, self.last_name)

    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')
 
    def get_absolute_url(self):
        return reverse('author-detail', kwargs={'pk': self.pk})       


@python_2_unicode_compatible
class Publisher(models.Model):
    name = models.CharField(verbose_name=_('name'), max_length=100)

    def __str__(self):
        return self.name 

    class Meta:
        verbose_name = _('Publisher')
        verbose_name_plural = _('Publishers')


@python_2_unicode_compatible
class Genre(models.Model):
    name = models.CharField(verbose_name=_('name'), max_length=100)
    code = models.CharField(verbose_name=_('code'), max_length=10)

    def __str__(self):
        return '{} {}'.format(self.code ,self.name)

    class Meta:
        ordering = ('code',)
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')


@python_2_unicode_compatible
class Book(models.Model):
    AVALAIBLE = 'D'
    LENT = 'P'
    LOAN_STATUS_CHOICES = (
        (AVALAIBLE, _('Available')),
        (LENT, _('Lent')),
    )
    title = models.CharField(verbose_name=_('title'), max_length=200, unique=False)
    author = models.ManyToManyField(Author, verbose_name='author')
    publisher = models.ForeignKey(
        Publisher, verbose_name=_('publisher'),
        blank=True, null=True,
        on_delete=models.CASCADE, related_name='publishers'
    )
    genre = models.ForeignKey(
        Genre, verbose_name=_('genre'),
        blank=True, null=True,
        on_delete=models.CASCADE,
        related_name='genres'
    )
    column = models.IntegerField(verbose_name=_('column'))
    palco = models.CharField(verbose_name=_('palco'), max_length=4, blank=True, null=True)
    number = models.IntegerField(verbose_name=_('number'))
    year_edition = models.IntegerField(verbose_name=_('year edition'), blank=True,null=True)
    reprint_year = models.IntegerField(verbose_name=_('reprint year'), blank=True,null=True)
    main_topic = models.CharField(verbose_name=_('main topic'), max_length=200 , blank=True)
    secondary_topic = models.CharField(verbose_name=_('secondary topic'), max_length=200, blank=True)
    notes = models.CharField(verbose_name=_('notes'), max_length=200, blank=True)
    loan_status = models.CharField(max_length=100, choices=LOAN_STATUS_CHOICES, default='D')

    def __str__(self):
        return self.title  

    def get_absolute_url(self):
        return reverse('book-detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = _('Book')
        verbose_name_plural = _('Books')


@python_2_unicode_compatible
class Loan(models.Model):
    loan_holder = models.CharField(verbose_name=_('loan holder'), max_length=150, blank=True)
    loan_date = models.DateTimeField(verbose_name=_('loan date'), blank=True, null=True) 
    book = models.ForeignKey(Book, verbose_name=_('book'), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Loan')
        verbose_name_plural = _('Loans')


class Website(models.Model):
    url = models.URLField(max_length=200)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.url

    class Meta:
        verbose_name = 'Website'
        verbose_name_plural = 'Websites'
