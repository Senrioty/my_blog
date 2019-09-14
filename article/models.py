from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ArticleColumn(models.Model):
    title = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    column = models.ForeignKey(ArticleColumn, on_delete=models.CASCADE, null=True, blank=True, related_name='article')
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    # PositiveIntegerField 是用于存储正整数的字段
    total_views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_time']

    def __str__(self):
        return "<Article: %s>" % self.title



