from django.db import models
from django.contrib.auth.models import User
from article.models import Article
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey


# 未使用树形结构的Comment模型
# class Comment(models.Model):
#     article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
#
#     # 未使用富文本的定义
#     # content = models.TextField()
#
#     # 使用富文本
#     content = RichTextField()
#
#     created_time = models.DateTimeField(auto_now_add=True)
#     updated_time = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         ordering = ['-created_time']
#
#     def __str__(self):
#         return '<Comment: %s>' % self.content[:20]


# 替换 models.Model 为 MPTTModel
class Comment(MPTTModel):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    # 使用富文本
    content = RichTextField()

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    # mptt树形结构
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    # 记录二级评论回复给谁
    reply_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='replyers')

    # 替换Meta为MPTTMeat
    class MPTTMeta:
        order_insertion_by = ['created_time']

    def __str__(self):
        return '<Comment: %s>' % self.content[:20]