from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField

class Inedito(models.Model):
    titolo = models.CharField(max_length=200)  # Aggiunto max_length
    trama = models.TextField()
    autore = models.ForeignKey(User, on_delete=models.CASCADE)
    cover = models.ImageField(upload_to='covers/', null=True, blank=True)
    GENRE_CHOICES = [
        ('fantasy', 'Fantasy'),
        ('thriller', 'Thriller'),
        ('romance', 'Romance'),
    ]
    genere = MultiSelectField(choices=GENRE_CHOICES, max_length=100, blank=True)
    numero_pagine = models.IntegerField(default=1)


    def __str__(self):
        return f"{self.titolo} - {self.autore}"
   