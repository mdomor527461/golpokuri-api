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
    read_count = models.IntegerField(default=0, blank=True, null=True)
    writer = models.ForeignKey(User, related_name='stories_written', blank=True,on_delete=models.CASCADE,null=True)
    reader = models.ManyToManyField(User,related_name='readers',blank=True)
    def __str__(self):
        return self.title
   

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
        unique_together = ['user', 'story'] 
        
class StoryRating(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE , related_name='ratings')
    rating = models.IntegerField()
    
    
    def __str__(self):
        return f"{self.rating} star rated by {self.user}"
        
class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user.username} at {self.created_at}"



class CommentReaction(models.Model):
    REACTION_TYPES = [
        ('like', 'Like'),
        ('love', 'Love'),
        ('angry', 'Angry'),
        ('haha', 'Haha'),
        ('wow', 'wow'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name='reactions', on_delete=models.CASCADE)
    type = models.CharField(choices=REACTION_TYPES, max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Reaction by {self.user.username} on Comment {self.comment.id}"

