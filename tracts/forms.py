from django import forms

from .models import Tract

class TractForm(forms.ModelForm):
    class Meta:
        model = Tract
        fields = ('short_legal', 'full_legal', 'situs_address',
                  'city', 'state', 'zip_code',
        )
        widgets = {
            'short_legal': forms.TextInput(
                attrs={
                    'placeholder':'Short Legal',
                    'class':'col-md-12 form-control'
                }
            ),
            'full_legal': forms.Textarea(
                attrs={
                    'placeholder':'Enter full legal description',
                    'class':'form-control'
                }
            ),
            'situs_address': forms.TextInput(
                attrs={
                    'placeholder':'Situs Address',
                    'class':'gi-form-addr form-control'
                }
            ),
            'city': forms.TextInput(
                attrs={
                    'placeholder':'City',
                    'class':'gi-form-addr form-control'
                }
            ),
            'state': forms.TextInput(
                attrs={
                    'placeholder':'State',
                    'class':'gi-form-addr form-control'
                }
            ),
            'zip_code': forms.TextInput(
                attrs={
                    'placeholder':'Zip Code',
                    'class':'gi-form-addr form-control'
                }
            ),
        }
