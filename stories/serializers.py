from rest_framework import serializers
from . import models
from django.db.models import Count
from users.serializers import UserSerializer
from rest_framework import serializers
from .models import StoryReact
class StorySerializer(serializers.ModelSerializer):
    writer = UserSerializer()
    reader = UserSerializer(many=True)
    category_name = serializers.StringRelatedField(source='category')
    react_counts = serializers.SerializerMethodField()
    user_reaction = serializers.SerializerMethodField()
    user_rating = serializers.SerializerMethodField()
    all_user_reacts = serializers.SerializerMethodField()
    class Meta:
        model = models.Story
        fields = ['id','title','image_url','content','category','category_name','react_counts','reader','read_count','writer','user_reaction','all_user_reacts','total_reviews','average_rating','user_rating']

    def get_category(self, obj):
        return obj.category.name
    
    def get_react_counts(self, obj):
        return obj.reacts.values('type').annotate(count=Count('id'))
    
    def get_user_reaction(self,obj):
        user = self.context['request'].user
        react = obj.reacts.filter(user = user).first()
        
        if react:
            return {
                'id': react.id,
                'type': react.type
            }
        return None
    def get_user_rating(self,obj):
        user = self.context['request'].user
        rating = obj.ratings.filter(user = user).first()
        
        if rating:
            return {
                'id': rating.id,
                'rating_number': rating.rating
            }
        return None

    
    def get_all_user_reacts(self, obj):
        reacts = obj.reacts.select_related('user').all()
        return [
            {
                'id': react.id,
                'user_id': react.user.id,
                'username': react.user.username,
                'image': react.user.image.url if react.user.image else None,
                'reaction': react.type,
                'reacted_at': react.reacted_at
            }
            for react in reacts
        ]

 
class TopStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Story
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    # image_url = serializers.ImageField()
    class Meta:
        model = models.Category
        fields = '__all__'
        


class StoryReactSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryReact
        fields = ['id', 'story', 'type', 'reacted_at']
        read_only_fields = ['id', 'reacted_at']

    def create(self, validated_data):
        user = self.context['request'].user
        story = validated_data['story']
        type = validated_data['type']

        # Update if already exists
        react, created = StoryReact.objects.update_or_create(
            user=user,
            story=story,
            defaults={'type': type}
        )
        return react


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ['id', 'content', 'user', 'parent', 'created_at','story']

class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CommentReaction
        fields = ['id', 'user', 'comment', 'type', 'created_at']
        
class StoryRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StoryRating
        fields = '__all__'