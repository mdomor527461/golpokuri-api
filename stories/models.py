from django.db import models
from django.conf import settings
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='categories', null=True, blank=True)
    def __str__(self):
        return self.name
    
class Story(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='stories',null=True,blank=True)

    def __str__(self):
        return self.title
class Comment(models.Model):
    content = models.TextField()
    story = models.ForeignKey(Story,on_delete=models.CASCADE)

    def __str__(self):
        return self.content