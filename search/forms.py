from django import forms
# -*- coding: utf-8 -*-
class SearchForm(forms.Form):
    subdivision = forms.CharField(
        label='Enter A Subdivision'
    )
    block = forms.CharField(
        label='Enter A Block'
    )
