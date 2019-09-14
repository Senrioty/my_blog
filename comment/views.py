from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from article.models import Article
from .form import CommentForm


# Create your views here.

@login_required(login_url='userprofile/login')
def post_comment(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user
            new_comment.save()

            # 当其参数是一个Model对象时，会自动调用这个Model对象的get_absolute_url()方法
            return redirect(article)
        else:
            return HttpResponse("表单内容有误，请重新填写")