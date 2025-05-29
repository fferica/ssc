from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

GENDER_CHOICES = [
    ('M', 'Maschio'),
    ('F', 'Femmina'),
    ('NB', 'Non binari*'),
    ('ALTRO', 'Altro'),
]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profilo')
    gender = models.CharField(max_length=5, choices=GENDER_CHOICES)
    already_published = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s profilo"
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        if hasattr(instance, 'profilo'):
            instance.profile.save()

