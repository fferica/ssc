from django.db import models
from django.contrib.auth.models import User

GENDER_CHOICES = [
    ('M', 'Maschio'),
    ('F', 'Femmina'),
    ('NB', 'Non binari*'),
    ('ALTRO', 'Altro'),
]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    gender = models.CharField(max_length=5, choices=GENDER_CHOICES)
    already_published = models.BooleanField(default=False)

    def __str__(self):
        return f"Profile of {self.user.username}"
