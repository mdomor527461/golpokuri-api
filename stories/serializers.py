from rest_framework import serializers
from . import models
from django.db.models import Count
from users.serializers import UserSerializer
class StorySerializer(serializers.ModelSerializer):
    writer = UserSerializer()
    reader = UserSerializer(many=True)
    category_name = serializers.StringRelatedField(source='category')
    react_counts = serializers.SerializerMethodField()
    user_reaction = serializers.SerializerMethodField()
    class Meta:
        model = models.Story
        fields = ['id','title','image_url','content','category','category_name','react_counts','reader','read_count','writer','user_reaction']

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

class CategorySerializer(serializers.ModelSerializer):
    # image_url = serializers.ImageField()
    class Meta:
        model = models.Category
        fields = '__all__'
class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.StringRelatedField(source='user')
    class Meta:
        model = models.Comment
        fields = ['user_name','content']
        
      
class ReviewSerilizer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at']
        
        def create(self, validated_data):
            validated_data['user'] = self.context['request'].user
            return super().create(validated_data)
        
from rest_framework import serializers
from .models import StoryReact

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
