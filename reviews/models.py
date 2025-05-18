from django.db import models


from django.db import models
from books.models import Book
from accounts.models import User

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()  
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('book', 'user') 

    def __str__(self):
        return f"{self.user.name} - {self.book.title} ({self.rating}★)"
