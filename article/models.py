from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from PIL import Image
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
from django.urls import reverse
from django.utils import timezone

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

    # 使用pillow处理，需要在save()方法中对图片进行处理
    # avatar = models.ImageField(upload_to='article/%Y%m%d', blank=True)

    # 使用更高级的库django-imagekit来处理图片，直接在定义字段就可以给出处理图片的说明
    avatar = ProcessedImageField(
        upload_to='article/%Y%m%d',
        processors=[ResizeToFit(width=400)],
        format='JPEG',
        options={'quality':100},
        blank=True
    )

    # 点赞
    likes = models.PositiveIntegerField(default=0)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    # PositiveIntegerField 是用于存储正整数的字段
    total_views = models.PositiveIntegerField(default=0)

    # 应用第三方库django-taggit实现标签功能,这是多对多
    tags = TaggableManager(blank=True)

    class Meta:
        ordering = ['-created_time']

    def __str__(self):
        return "<Article: %s>" % self.title

    # def save(self, *args, **kwargs):
    #     # 调用原有的save()方法
    #     article = super(Article, self).save(*args, **kwargs)
    #
    #     # 处理图片
    #     # 第一个判断是过滤没有缩略图的，自然就不用处理；
    #     # 第二个判断是过滤之前做浏览量统计时只更新total_views字段的操作，即save(update_fields=['total_views'])
    #     if self.avatar and not kwargs.get('update_fields'):
    #         image = Image.open(self.avatar)
    #         (x, y) = image.size
    #         new_x = 400
    #         new_y = int(new_x * (y / x))
    #         resized_image = image.resize((new_x, new_y), Image.ANTIALIAS)  # Image.ANTIALIAS表示缩放采用平滑滤波
    #         resized_image.save(self.avatar.path)  # 覆盖掉原始图片
    #
    #     return article


    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id])

    def was_created_centenly(self):
        diff = timezone.now() - self.created_time
        if diff.days ==0 and diff.seconds >= 0 and diff.seconds <= 60:
            return True
        else:
            return False