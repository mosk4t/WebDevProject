from rest_framework import serializers
from .models import Book, Comment, LikeDislike, License
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password], style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')
        extra_kwargs = {'email': {'required': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Email already exists."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'description', 'published_at']

class BookStatsSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
    title = serializers.CharField()
    total_comments = serializers.IntegerField()
    total_likes = serializers.IntegerField()
    total_dislikes = serializers.IntegerField()
    average_rating = serializers.FloatField(allow_null=True)

    def validate_book_id(self, value):
        if not Book.objects.filter(id=value).exists():
            raise serializers.ValidationError("Book with this ID does not exist.")
        return value

class UserProfileSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    join_date = serializers.DateTimeField(source='date_joined')
    is_active = serializers.BooleanField()
    book_count = serializers.SerializerMethodField()

    def get_book_count(self, obj):
        return Book.objects.filter(author=obj).count()

class CommentSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'book', 'user', 'user_username', 'content', 'created_at']
        extra_kwargs = {
            'user': {'read_only': True},
            'book': {'read_only': True}
        }

class LikeDislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeDislike
        fields = ['id', 'book', 'user', 'like']
        extra_kwargs = {
            'user': {'read_only': True},
            'book': {'read_only': True}
        }

class LicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = License
        fields = ['user', 'is_author', 'awarded_at']
        extra_kwargs = {
            'user': {'read_only': True},
            'awarded_at': {'read_only': True}
        }