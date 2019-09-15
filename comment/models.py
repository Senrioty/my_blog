from django.db import models
from django.contrib.auth.models import User
from article.models import Article
from ckeditor.fields import RichTextField


# Create your models here.
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    # 未使用富文本的定义
    # content = models.TextField()

    # 使用富文本
    content = RichTextField()

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_time']

    def __str__(self):
        return '<Comment: %s>' % self.content[:20]