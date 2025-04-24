from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from .models import Book, Comment, License
from .serializers import BookSerializer, CommentSerializer, UserRegistrationSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "User registered successfully",
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Login successful",
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }, status=status.HTTP_200_OK)
        return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_books(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

def book_comments(request, book_id):
    comments = Comment.objects.filter(book_id=book_id)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


class CommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        content = request.data.get('content')
        if not content:
            return Response({"message": "Content is required."}, status=status.HTTP_400_BAD_REQUEST)
        comment = Comment.objects.create(book=book, user=request.user, content=content)
        return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_comment(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    content = request.data.get('content')
    if not content:
        return Response({"message": "Content is required."}, status=status.HTTP_400_BAD_REQUEST)
    comment = Comment.objects.create(book=book, user=request.user, content=content)
    return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user != request.user:
        return Response({"message": "You can only edit your own comments."}, status=status.HTTP_403_FORBIDDEN)
    content = request.data.get('content')
    if not content:
        return Response({"message": "Content is required."}, status=status.HTTP_400_BAD_REQUEST)
    comment.content = content
    comment.save()
    return Response(CommentSerializer(comment).data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user != request.user:
        return Response({"message": "You can only delete your own comments."}, status=status.HTTP_403_FORBIDDEN)
    comment.delete()
    return Response({"message": "Comment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class LicenseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user_license = License.objects.get(user=request.user)
            if user_license.is_author:
                return Response({"message": "You are an author."})
            return Response({"message": "License processing logic here"}, status=status.HTTP_200_OK)
        except License.DoesNotExist:
            return Response({"message": "License not found for this user."}, status=status.HTTP_404_NOT_FOUND)