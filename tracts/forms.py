from django import forms

from .models import Tract

class TractForm(forms.ModelForm):
    class Meta:
        model = Tract
        fields = ('short_legal', 'full_legal', 'situs_address',
                  'city', 'state', 'zip_code', 'acreage', 'status',
        )
        widgets = {
            'short_legal': forms.TextInput(
                attrs={
                    'placeholder':'Short Legal',
                    'class':'form-control'
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
                    'class':'form-control'
                }
            ),
            'city': forms.TextInput(
                attrs={
                    'placeholder':'City',
                    'class':'form-control'
                }
            ),
            'state': forms.TextInput(
                attrs={
                    'placeholder':'State',
                    'class':'form-control'
                }
            ),
            'zip_code': forms.TextInput(
                attrs={
                    'placeholder':'Zip Code',
                    'class':'form-control'
                }
            ),
            'acreage': forms.TextInput(
                attrs={
                    'placeholder':'Acreage',
                    'class':'form-control'
                }
            ),
            'status': forms.TextInput(
                attrs={
                    'placeholder':'Status',
                    'class':'form-control'
                }
            ),
        }
