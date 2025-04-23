# books/urls.py
from django.urls import path
from . import views
from .views import RegisterView, get_books, CommentView, LicenseView, LoginView,add_comment

urlpatterns = [
    path('books/', views.get_books),
    path('comments/<int:book_id>/', views.CommentView.as_view()),
    path('license/', views.LicenseView.as_view()),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'), 
    path('books/<int:book_id>/comments/', views.add_comment, name='add_comment'),
     path('comments/<int:comment_id>/update/', views.update_comment, name='update_comment'),  # For updating comment
    path('comments/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'), 
]
