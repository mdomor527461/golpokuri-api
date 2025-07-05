from django.db import models
from users.models import User
from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import math

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    def __str__(self):
        return self.name
    
class Story(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image_url = models.URLField(max_length=500, blank=True, null=True) 
    total_reviews = models.IntegerField(default=0,null=True,blank=True)
    average_rating = models.IntegerField(default=0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)
    def update_rating(self):
        reviews = self.reviews.all()
        
        if reviews.exists():
            avg = sum([r.rating for r in reviews]) / reviews.count()
            self.average_rating = math.ceil(avg)
            self.total_reviews = reviews.count()
        else:
            self.average_rating = 0
            self.total_reviews = 0
            
    read_count = models.IntegerField(default=0, blank=True, null=True)
    writer = models.ForeignKey(User, related_name='stories_written', blank=True,on_delete=models.CASCADE,null=True)
    reader = models.ManyToManyField(User,related_name='readers',blank=True)
    def __str__(self):
        return self.title
    

class Comment(models.Model):
    content = models.TextField()
    story = models.ForeignKey(Story,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)

    def __str__(self):
        return self.content

class Review(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        unique_together = ['story', 'user']  # each user can review once

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.story.update_rating()
        
class StoryReact(models.Model):
    REACT_CHOICES = [
        ('like', 'Like'),
        ('love', 'Love'),
        ('dislike', 'Dislike'),
        ('wow', 'Wow'),
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    story = models.ForeignKey(Story,on_delete=models.CASCADE ,  related_name='reacts')
    type = models.CharField(choices=REACT_CHOICES, max_length=10)
    reacted_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'story']  # ১ user ১টা react দিতে পারবে প্রতি story-তে