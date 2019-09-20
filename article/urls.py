from django.urls import path
from . import views

# Django2.0之后，app的urls.py必须配置app_name，否则会报错
app_name = 'article'

urlpatterns = [
    path('', views.article_list, name='article_list'),
    # path('', views.ArticleListView.as_view(), name='article_list'),
    path('article_detail/<int:id>', views.article_detail, name='article_detail'),
    path('article_create/', views.article_create, name='article_create'),
    path('article_delete/<int:id>', views.article_delete, name='article_delete'),
    path('article_safe_delete/<int:id>', views.article_safe_delete, name='article__safe_delete'),
    path('article_update/<int:id>', views.article_update, name='article_update'),
    path('increase_likes/<int:id>', views.IncreaseLikeView.as_view(), name='increase_likes'),
]
