# books/serializers.py
from rest_framework import serializers
from .models import Book, Comment, LikeDislike, License

from django.contrib.auth.models import User
from rest_framework import serializers


# books/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'description', 'published_at']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'book', 'user', 'content', 'created_at']

class LikeDislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeDislike
        fields = ['id', 'book', 'user', 'like']

class LicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = License
        fields = ['user', 'is_author', 'awarded_at']
