from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('writer', 'Writer'),
        ('reader', 'Reader'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    image = models.ImageField(upload_to='users',null=True,blank=True)
    def __str__(self):
        return self.username

