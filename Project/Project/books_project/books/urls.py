from django.urls import path
from .views import (
    RegisterView, 
    get_books, 
    CommentView, 
    LicenseView, 
    LoginView, 
    add_comment, 
    update_comment, 
    delete_comment,
    book_comments
)

urlpatterns = [
    path('books/', get_books, name='get-books'),
    path('comments/<int:book_id>/', CommentView.as_view(), name='comment-list'),
    path('license/', LicenseView.as_view(), name='license'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('books/<int:book_id>/comments/', add_comment, name='add-comment'),
    path('comments/<int:comment_id>/update/', update_comment, name='update-comment'),
    path('comments/<int:comment_id>/delete/', delete_comment, name='delete-comment'),
    path('api/books/<int:book_id>/comments/', book_comments, name='book-comments')
]