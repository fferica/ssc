from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

GENDER_CHOICES = [
    ('M', 'Maschio'),
    ('F', 'Femmina'),
    ('NB', 'Non binari*'),
    ('ALTRO', 'Altro'),
]

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label='Nome')
    last_name = forms.CharField(max_length=30, required=True, label='Cognome')
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=True, label='Genere')
    already_published = forms.BooleanField(required=False, label='Hai già pubblicato libri?')
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'gender', 'already_published', 'password1', 'password2']
