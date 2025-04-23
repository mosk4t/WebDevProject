# books/models.py
from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    published_at = models.DateField()

    def __str__(self):
        return self.title

class Comment(models.Model):
    book = models.ForeignKey(Book, related_name='comments', on_delete=models.CASCADE)  # ForeignKey к книге
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)  # ForeignKey к пользователю
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.book.title}"

class LikeDislike(models.Model):
    book = models.ForeignKey(Book, related_name='likes_dislikes', on_delete=models.CASCADE)  # ForeignKey к книге
    user = models.ForeignKey(User, related_name='likes_dislikes', on_delete=models.CASCADE)  # ForeignKey к пользователю
    like = models.BooleanField(default=True)

    class Meta:
        unique_together = ['book', 'user']

class License(models.Model):
    user = models.OneToOneField(User, related_name='license', on_delete=models.CASCADE)  # OneToOne связь с пользователем
    is_author = models.BooleanField(default=False)
    awarded_at = models.DateTimeField(null=True, blank=True)

class FavouriteBook(models.Model):
    user = models.ForeignKey(User, related_name='favourite_books', on_delete=models.CASCADE)  # ForeignKey к пользователю
    book = models.ForeignKey(Book, related_name='favourited_by', on_delete=models.CASCADE)  # ForeignKey к книге
    added_at = models.DateTimeField(auto_now_add=True)  # Дата добавления в избранное

    class Meta:
        unique_together = ['user', 'book']  # Каждая книга может быть в избранном у пользователя только один раз

    def __str__(self):
        return f"{self.user.username}'s favourite book: {self.book.title}"
