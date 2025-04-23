# books/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Book, Comment, LikeDislike, License
from .serializers import BookSerializer, CommentSerializer, LikeDislikeSerializer, LicenseSerializer
from rest_framework.permissions import IsAuthenticated
# views.py в Django
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
# books/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer
from rest_framework.permissions import AllowAny 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer
from rest_framework.permissions import AllowAny

class RegisterView(APIView):
    permission_classes = [AllowAny]  # Разрешаем доступ всем

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# Функциональные представления для получения всех книг
@api_view(['GET'])
def get_books(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

# Класс для добавления комментариев
class CommentView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, book_id):
        book = Book.objects.get(id=book_id)
        content = request.data.get('content')
        comment = Comment.objects.create(book=book, user=request.user, content=content)
        return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def add_comment(request, book_id):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return Response({"message": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

    # Retrieve the book based on the provided book_id
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return Response({"message": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

    # Get the content from the request data
    content = request.data.get('content')

    if not content:
        return Response({"message": "Content is required."}, status=status.HTTP_400_BAD_REQUEST)

    # Create a new comment
    comment = Comment.objects.create(book=book, user=request.user, content=content)

    # Serialize the comment and return the response
    return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
def update_comment(request, comment_id):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return Response({"message": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return Response({"message": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)

    # Ensure the user is the one who posted the comment
    if comment.user != request.user:
        return Response({"message": "You can only edit your own comments."}, status=status.HTTP_403_FORBIDDEN)

    # Get the new content from the request data
    content = request.data.get('content')

    if not content:
        return Response({"message": "Content is required."}, status=status.HTTP_400_BAD_REQUEST)

    # Update the comment
    comment.content = content
    comment.save()

    return Response(CommentSerializer(comment).data, status=status.HTTP_200_OK)


# Delete a comment
@api_view(['DELETE'])
def delete_comment(request, comment_id):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return Response({"message": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return Response({"message": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)

    # Ensure the user is the one who posted the comment
    if comment.user != request.user:
        return Response({"message": "You can only delete your own comments."}, status=status.HTTP_403_FORBIDDEN)

    # Delete the comment
    comment.delete()

    return Response({"message": "Comment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
class LoginView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            # Здесь возвращаем токен или другие данные
            return Response({"message": "Login successful", "token": "your_jwt_token"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
class LicenseView(APIView):
    def post(self, request):
        user_license = License.objects.get(user=request.user)
        if user_license.is_author:
            return Response({"message": "You are an author."})
        else:
            # Логика присвоения лицензии
            pass
