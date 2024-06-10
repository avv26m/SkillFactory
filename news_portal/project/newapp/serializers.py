from .models import *
from rest_framework import serializers

class NewsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'author', 'categoryType', 'dateCreation', 'title', 'text', 'rating']

class ArticlesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'author', 'categoryType', 'dateCreation', 'title', 'text', 'rating']

class AutorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ['id',]

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        field = ['id', 'name']

class PostCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PostCategory
        field = ['id',]

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        field = ['id', 'text', 'dateCreation', 'rating']