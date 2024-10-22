from rest_framework import serializers
from . import models
class StorySerializer(serializers.ModelSerializer):
    writer = serializers.StringRelatedField(read_only=True)
    category_name = serializers.StringRelatedField(source='category')
    class Meta:
        model = models.Story
        fields = ['id','title','image_url','content','date_posted','category','category_name','writer']

    def get_category(self, obj):
        return obj.category.name
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     if instance.image:
    #         representation['image'] = instance.image.url
    #     return representation

class CategorySerializer(serializers.ModelSerializer):
    image_url = serializers.ImageField()
    class Meta:
        model = models.Category
        fields = '__all__'
class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.StringRelatedField(source='user')
    class Meta:
        model = models.Comment
        fields = ['user_name','content']