from .models import *
from rest_framework import serializers

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'author', 'categoryType','postCategory', 'dateCreation', 'title', 'text', 'rating']

class ArticlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'author', 'categoryType', 'dateCreation', 'title', 'text', 'rating']

class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id',]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        field = ['id', 'name']

class PostCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCategory
        field = ['id',]

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        field = ['id', 'text', 'dateCreation', 'rating']