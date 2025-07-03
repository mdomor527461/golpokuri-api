from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
   
    image = models.ImageField(upload_to='users',null=True,blank=True)
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = 'email'  # ✅ This is key
    REQUIRED_FIELDS = []
    

    
    def __str__(self):
        return self.username

