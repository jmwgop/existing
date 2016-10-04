from django import forms
# -*- coding: utf-8 -*-
class SearchForm(forms.Form):
    subdivision = forms.CharField(
        label='Enter A Subdivision'
    )
    block = forms.CharField(
        label='Enter A Block'
    )


class SecSearch(forms.Form):
    section = forms.CharField(
        label='Enter A Subdivision'
    )
    block = forms.CharField(
        label='Enter A Block'
    )
    township = forms.CharField(
        label='Enter A Block'
    )
