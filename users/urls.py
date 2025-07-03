from django.urls import path
from .views import UserCreateView
from . import views

urlpatterns = [
    path('register/', views.UserCreateView.as_view(), name='user-register'),
    path('login/', views.UserLoginApiView.as_view(), name='user-login'),
    path('logout/', views.UserLogoutView.as_view(), name='user-logout'),
]