from django.shortcuts import render
from rest_framework import generics
from . import models
from . import serializers
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.
class StoryCreateView(generics.CreateAPIView):
    queryset = models.Story.objects.all()
    serializer_class = serializers.StorySerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        if self.request.user.user_type == 'writer':
            subject = 'Story Creating successful message'
            message = f'Congratulations {self.request.user.username} your story succussfully uploaded at golpkuri'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [self.request.user.email]
            send_mail( subject, message, email_from, recipient_list)
            serializer.save(writer=self.request.user)
        else:
            raise PermissionDenied({"error": "Only writers can create story"})
  

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
class StoryDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = models.Story.objects.all()
    serializer_class = serializers.StorySerializer

class StoryUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.StorySerializer
    queryset = models.Story.objects.all()

class StoryDeleteView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.StorySerializer
    queryset = models.Story.objects.all()

class CategoryListView(generics.ListAPIView):
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()

    










    