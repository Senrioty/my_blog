from django.urls import path
from . import views

# Django2.0之后，app的urls.py必须配置app_name，否则会报错
app_name = 'notice'



urlpatterns = [
    # 因为path第二个参数只接受函数，所以类视图要添加一个as_view()的方法

    path('list/', views.CommentNoticeListView.as_view(), name='list'),
    path('update/', views.CommentNoticeUpdateView.as_view(), name='update'),
]
