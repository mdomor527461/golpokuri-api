from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login, logout
from .models import User
from .serializers import UserSerializer, UserLoginSerializer, GoogleAuthSerializer
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.conf import settings

class UserCreateView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserLoginApiView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        if request.content_type == 'application/json':
            data = request.data
        else:
            data = request.POST

        serializer = UserLoginSerializer(data=data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            user = authenticate(request, email=email, password=password)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                login(request, user)
                return Response({
                    'token': token.key,
                    'user_id': user.id,
                    'email': user.email,
                    'username':user.username
                })
            else:
                return Response({'error': "Invalid Credentials"}, status=400)
        
        return Response(serializer.errors, status=400)


class UserLogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"detail": "Logged out successfully"}, status=200)

