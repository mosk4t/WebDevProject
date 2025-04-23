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
    permission_classes = [IsAuthenticated]

    def post(self, request, book_id):
        book = Book.objects.get(id=book_id)
        content = request.data.get('content')
        comment = Comment.objects.create(book=book, user=request.user, content=content)
        return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)

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
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_license = License.objects.get(user=request.user)
        if user_license.is_author:
            return Response({"message": "You are an author."})
        else:
            # Логика присвоения лицензии
            pass
