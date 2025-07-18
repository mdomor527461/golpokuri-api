from django.shortcuts import render
from rest_framework import generics
from . import models
from . import serializers
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.conf import settings
from django.core.mail import send_mail
import requests
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets, permissions
import math
from rest_framework.views import APIView
# Create your views here.

IMAGEBB_API_KEY = 'bd168c98953ad999e53d8ca206d477fa'

class StoryCreateView(generics.CreateAPIView):
    serializer_class = serializers.StorySerializer
    permission_classes = [IsAuthenticated]
    def post(self, request):
        # প্রথমে সিরিয়ালাইজার থেকে ডাটা গ্রহণ করা
        serializer = serializers.StorySerializer(data=request.data)

        if serializer.is_valid():
            story = serializer.save(writer=request.user)

            # যদি ফাইল থাকে তবে ImageBB তে আপলোড করা হবে
            image_file = request.FILES.get('image', None)
            if image_file:
                url = "https://api.imgbb.com/1/upload"
                files = {
                    'image': image_file,
                }
                data = {
                    'key': IMAGEBB_API_KEY,
                }

                # API তে রিকুয়েস্ট পাঠানো
                response = requests.post(url, data=data, files=files)

                # যদি রিকুয়েস্ট সফল হয় তাহলে image_url আপডেট করা
                if response.status_code == 200:
                    image_url = response.json()['data']['url']
                    story.image_url = image_url
                    story.save()

            return Response(serializers.StorySerializer(story).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  

class StoryListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.StorySerializer

    def get_queryset(self):
        category_id = self.request.query_params.get('category',None)
        writer_id = self.request.query_params.get('writer',None)
        if writer_id is not None :
            return models.Story.objects.filter(writer_id = writer_id)
        if category_id is not None:
            return models.Story.objects.filter(category__id = category_id)
        return models.Story.objects.all()


class TopStoryListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.TopStorySerializer
    
    def get_queryset(self):
        return models.Story.objects.order_by('-read_count')[:8]
    
class StoryDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = models.Story.objects.all()
    serializer_class = serializers.StorySerializer

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        story = self.get_object()

        if request.user not in story.reader.all():
            story.reader.add(request.user)
            story.read_count += 1
            story.save(update_fields=['read_count'])

        return response

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class StoryUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.StorySerializer
    queryset = models.Story.objects.all()

class StoryDeleteView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.StorySerializer
    queryset = models.Story.objects.all()
class CategoryCreateView(generics.CreateAPIView):
    serializer_class = serializers.CategorySerializer
    permission_classes = [IsAdminUser]
    def post(self, request):
        # প্রথমে সিরিয়ালাইজার থেকে ডাটা গ্রহণ করা
        serializer = serializers.CategorySerializer(data=request.data)

        if serializer.is_valid():
            category = serializer.save()

            # যদি ফাইল থাকে তবে ImageBB তে আপলোড করা হবে
            image_file = request.FILES.get('image', None)
            if image_file:
                url = "https://api.imgbb.com/1/upload"
                files = {
                    'image': image_file,
                }
                data = {
                    'key': IMAGEBB_API_KEY,
                }

                # API তে রিকুয়েস্ট পাঠানো
                response = requests.post(url, data=data, files=files)

                # যদি রিকুয়েস্ট সফল হয় তাহলে image_url আপডেট করা
                if response.status_code == 200:
                    image_url = response.json()['data']['url']
                    category.image_url = image_url
                    category.save()

            return Response(serializers.CategorySerializer(category).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class CategoryListView(generics.ListAPIView):
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()


class StoryReactCreateUpdateView(generics.CreateAPIView):
    queryset = models.StoryReact.objects.all()
    serializer_class = serializers.StoryReactSerializer
    permission_classes = [permissions.IsAuthenticated]


class StoryReactDeleteView(generics.DestroyAPIView):
    queryset = models.StoryReact
    serializer_class  = serializers.StoryReactSerializer
    permission_classes = [permissions.IsAuthenticated]

class CommentListCreateView(generics.ListCreateAPIView):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CommentEditView(generics.UpdateAPIView):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        comment = super().get_object()
        if comment.user != self.request.user:
            raise PermissionError("You do not have permission to edit this comment.")
        return comment

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data['message'] = 'Comment updated successfully'
        return response
class CommentDeleteView(generics.DestroyAPIView):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        comment = super().get_object()
        if comment.user != self.request.user:
            raise PermissionError("You do not have permission to delete this comment.")
        return comment

class ReactionListCreateView(generics.ListCreateAPIView):
    queryset = models.CommentReaction.objects.all()
    serializer_class = serializers.ReactionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReactionDeleteView(generics.DestroyAPIView):
    queryset = models.CommentReaction.objects.all()
    serializer_class = serializers.ReactionSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        reaction = super().get_object()
        if reaction.user != self.request.user:
            raise PermissionError("You do not have permission to delete this reaction.")
        return reaction    
    

class StoryRatingCreateView(generics.ListCreateAPIView):
    queryset = models.StoryRating.objects.all()  # Queryset to fetch StoryRatings
    serializer_class = serializers.StoryRatingSerializer  # Serializer for StoryRating
    permission_classes = [IsAuthenticated]  # Ensures only authenticated users can create ratings

    def perform_create(self, serializer):
        # Check if the user has already rated the story
        user = self.request.user
        story = serializer.validated_data['story']  # Get the story from the validated data

        # Check if a rating already exists for this user and story
        existing_rating = models.StoryRating.objects.filter(user=user, story=story).first()

        if existing_rating:
            # If the rating already exists, update it
            existing_rating.rating = serializer.validated_data['rating']
            existing_rating.save()
            story_rating = existing_rating  # Use the existing rating
        else:
            # Otherwise, create a new rating
            story_rating = serializer.save(user=user)

        # Update the total_reviews and average_rating after the new or updated rating
        self.update_story_rating(story)

    def update_story_rating(self, story):
        # Update the total_reviews and average_rating after the rating is created or updated
        story.total_reviews = story.ratings.count()  # Count the total number of ratings for this story
        
        # Calculate the average_rating (if there are ratings)
        if story.total_reviews > 0:
            total_sum = sum(rating.rating for rating in story.ratings.all())  # Sum of all ratings
            story.average_rating = total_sum / story.total_reviews  # Calculate the average

        # Save the Story instance with the updated total_reviews and average_rating
        story.save()