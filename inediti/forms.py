from django import forms
from .models import Inedito

class IneditoForm(forms.ModelForm):
    class Meta:
        model = Inedito
        fields = ['titolo', 'trama', 'genere', 'autore', 'cover']
