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
    serializer_class = serializers.StorySerializer
    
    def get_queryset(self):
        return models.Story.objects.order_by('-read_count')[:8]
    
class StoryDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = models.Story.objects.all()
    serializer_class = serializers.StorySerializer

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        story = self.get_object()

        # Only count read if this user hasn't read it before
        if request.user not in story.reader.all():
            story.reader.add(request.user)        # Track the reader
            story.read_count += 1
            story.save(update_fields=['read_count'])  # Save only that field for performance

        return response

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
class CommentView(generics.ListCreateAPIView):
    serializer_class = serializers.CommentSerializer
    
    def get_queryset(self):
        story_id = self.kwargs['pk']  # URL থেকে স্টোরির ID নেওয়া হচ্ছে
        return models.Comment.objects.filter(story__id=story_id)  # নির্দিষ্ট স্টোরির কমেন্টগুলো ফিল্টার করা হচ্ছে

    def perform_create(self, serializer):
        story = models.Story.objects.get(pk=self.kwargs['pk'])  # নির্দিষ্ট স্টোরি পাওয়া হচ্ছে
        serializer.save(user=self.request.user, story=story) 


class ReviewCreateView(generics.CreateAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerilizer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        story = serializer.validated_data['story']

        # Check if this user already reviewed this story
        existing_review = models.Review.objects.filter(user=user, story=story).first()

        if existing_review:
            # Update existing review
            existing_review.rating = serializer.validated_data['rating']
            existing_review.comment = serializer.validated_data.get('comment', '')
            existing_review.save()
        else:
            # Create new review
            serializer.save(user=user)











    