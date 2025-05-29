from django import forms
from .models import Scaduto

class ScadutoForm(forms.ModelForm):
    class Meta:
        model = Scaduto
        fields = ['titolo', 'trama', 'anno_pubblicazione', 'editore', 'cover', 'numero_pagine']
