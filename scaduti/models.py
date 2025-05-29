from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField

class Scaduto(models.Model):
    titolo = models.CharField(max_length=200)
    trama = models.TextField()
    anno_pubblicazione = models.IntegerField()
    editore = models.CharField(max_length=100)
    autore = models.ForeignKey(User, on_delete=models.CASCADE)
    cover = models.ImageField(upload_to='covers/', null=True, blank=True)
    numero_pagine = models.IntegerField(default=1)
    
    GENRE_CHOICES = [
        ('fantasy', 'Fantasy'),
        ('thriller', 'Thriller'),
        ('romance', 'Romance'),
    ]
    genere = MultiSelectField(choices=GENRE_CHOICES, max_length=100, blank=True)

    def __str__(self):
        return f"{self.titolo} - {self.autore}"
