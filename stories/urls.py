from django.urls import path
from . import views


urlpatterns = [
    path('create/',views.StoryCreateView.as_view(),name='create'),
    path('stories/',views.StoryListView.as_view(),name='stories'),
    path('top_stories/',views.TopStoryListView.as_view(),name='top_stories'),
    path('stories/<int:pk>',views.StoryDetailView.as_view(),name='detail'),
    path('stories/edit/<int:pk>',views.StoryUpdateView.as_view(),name='update'),
    path('stories/delete/<int:pk>',views.StoryDeleteView.as_view(),name='delete'),
    path('categories/',views.CategoryListView.as_view(),name='categories'),
    path('category/create',views.CategoryCreateView.as_view(),name='create_category'),
    path('react/', views.StoryReactCreateUpdateView.as_view(), name='story-react'),
    path('react/delete/<int:pk>', views.StoryReactDeleteView.as_view(), name='story-react-delete'),
    # কমেন্ট সম্পর্কিত রাউট
    path('comments/', views.CommentListCreateView.as_view(), name='create_comment'),
    path('comments/<int:pk>/', views.CommentEditView.as_view(), name='edit_comment'),
    path('comments/delete/<int:pk>/', views.CommentDeleteView.as_view(), name='delete_comment'),

    # কমেন্ট রিয়্যাকশন সম্পর্কিত রাউট
    path('comment/react/', views.ReactionListCreateView.as_view(), name='create_reaction'),
    path('comment/react/delete/<int:pk>/', views.ReactionDeleteView.as_view(), name='delete_reaction'),
    
    #rating route
    path('rating/',views.StoryRatingCreateView.as_view(), name = 'story_rating'),
]