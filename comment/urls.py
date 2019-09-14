from django.urls import path
from . import views

# Django2.0之后，app的urls.py必须配置app_name，否则会报错
app_name = 'comment'

urlpatterns = [
    path('post_comment/<int:article_id>/', views.post_comment, name='post_comment')
]
