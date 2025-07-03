from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('create/',views.StoryCreateView.as_view(),name='create'),
    path('stories/',views.StoryListView.as_view(),name='stories'),
    path('top_stories/',views.TopStoryListView.as_view(),name='top_stories'),
    path('stories/<int:pk>',views.StoryDetailView.as_view(),name='detail'),
    path('stories/<int:pk>/comment',views.CommentView.as_view(),name='comment'),
    path('stories/edit/<int:pk>',views.StoryUpdateView.as_view(),name='update'),
    path('stories/delete/<int:pk>',views.StoryDeleteView.as_view(),name='delete'),
    path('categories/',views.CategoryListView.as_view(),name='categories'),
    path('category/create',views.CategoryCreateView.as_view(),name='create_category'),
    path('review/create',views.ReviewCreateView.as_view(),name='create_review'),
]