from django import forms
from django.utils.translation import gettext as _


class SearchBooksForm(forms.Form):
    title = forms.CharField(label=_('title'), required=False, max_length=100)