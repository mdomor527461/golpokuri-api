from django.urls import path
from .views import UserCreateView
from .views import UserLoginApiView,UserLogoutView

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('login/', UserLoginApiView.as_view(), name='api-login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]