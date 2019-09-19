import datetime

from time import sleep
from django.test import TestCase
from article.models import Article
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# 所有TestCase的子类都被认为是测试代码
class ArticleModelTests(TestCase):

    # 类中所有以test开头的方法会被认为是测试用例
    def test_was_created_recently_with_seconds_before_article(self):
        author = User(username='user1', password='test_password')
        author.save()

        future_article = Article(
            author=author,
            title='test1',
            content='test1',
            created_time=timezone.now() - datetime.timedelta(seconds=35)
        )

        self.assertIs(future_article.was_created_centenly(), True)

    def test_was_created_recently_with_hours_before_article(self):
        author = User(username='user2', password='test_password')
        author.save()

        future_article = Article(
            author=author,
            title='test2',
            content='test2',
            created_time=timezone.now() - datetime.timedelta(hours=3)
        )

        self.assertIs(future_article.was_created_centenly(), False)

    def test_was_created_recently_with_days_before_article(self):
        author = User(username='user3', password='test_password')
        author.save()

        future_article = Article(
            author=author,
            title='test3',
            content='test3',
            created_time=timezone.now() - datetime.timedelta(days=5)
        )

        self.assertIs(future_article.was_created_centenly(), False)


class ArticleViewTest(TestCase):

    def test_increase_views(self):
        author = User(username='user4', password='test_password')
        author.save()

        article = Article(
            author=author,
            title='test4',
            content='test4',
        )
        article.save()

        self.assertIs(article.total_views, 0)


        # 人为制造访问视图的代码
        url = reverse('article:article_detail', args=(article.id,))
        response = self.client.get(url)

        viewed_article = Article.objects.get(id=article.id)
        self.assertIs(viewed_article.total_views, 1)
