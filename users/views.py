from rest_framework import generics
from .models import User
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import redirect
from rest_framework.permissions import AllowAny
class UserCreateView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserLoginApiView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        # Check if the content type is JSON or Form Data
        if request.content_type == 'application/json':
            data = request.data
        else:  # If it's form data
            data = request.POST

        serializer = serializers.UserLoginSerializer(data=data)
        
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)
            
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                login(request, user)
                return Response({'token': token.key, 'user_id': user.id,'user_type': user.user_type})
            else:
                return Response({'error': "Invalid Credential"}, status=400)
        
        return Response(serializer.errors, status=400)
    
class UserLogoutView(APIView):
    def post(self, request):
        # request.user.auth_token.delete()  # If you're using token authentication
        logout(request)
        return Response({"detail": "Logged out successfully"}, status=200)