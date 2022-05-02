from django.db import models
from user.models import User
# Create your models here.


class Article(models.Model):
    def path_to(self, filename):
        return f'media/article/{self.id}/preview/{filename}'

    TYPE_CHOICES = (
        ("PUBLIC", "public"),
        ("PRIVATE", "private")
    )
    type = models.CharField(choices=TYPE_CHOICES, max_length=15)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    content = models.TextField()

    def get_author(self):
        return self.author
