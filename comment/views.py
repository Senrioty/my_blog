from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse,JsonResponse

from article.models import Article
from .form import CommentForm
from .models import Comment

from notifications.signals import notify



# Create your views here.

# 一级评论
# @login_required(login_url='userprofile/login')
# def post_comment(request, article_id):
#     article = get_object_or_404(Article, id=article_id)
#
#     if request.method == 'POST':
#         comment_form = CommentForm(request.POST)
#
#         if comment_form.is_valid():
#             new_comment = comment_form.save(commit=False)
#             new_comment.article = article
#             new_comment.user = request.user
#             new_comment.save()
#
#             # 当其参数是一个Model对象时，会自动调用这个Model对象的get_absolute_url()方法
#             return redirect(article)
#         else:
#             return HttpResponse("表单内容有误，请重新填写")


# 多级评论
@login_required(login_url='userprofile/login')
def post_comment(request, article_id, parent_comment_id=None):
    article = get_object_or_404(Article, id=article_id)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user

            # 二级评论
            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)

                # 若回复层级超过耳机，则转换为二级
                new_comment.parent_id = parent_comment.get_root().id

                # 被回复人
                new_comment.reply_to = parent_comment.user
                new_comment.save()

                # 给用户发起通知（会过滤掉管理员，避免重复接收）
                if not parent_comment.user.is_superuser:
                    notify.send(
                        request.user,
                        recipient=parent_comment.user,
                        verb='回复了你',
                        target=article,
                        action_object=new_comment
                    )

                # return HttpResponse('200 OK')

                # 特别提醒json格式必须用双引号
                return JsonResponse({"code":"200 OK", "new_comment_id":new_comment.id})

            new_comment.save()

            # 这个是给管理员发
            if not request.user.is_superuser:
                notify.send(
                    request.user,
                    recipient=User.objects.filter(is_superuser=1),
                    verb='回复了你',
                    target=article,
                    action_object=new_comment
                )


            # 发一级评论时，发完后应该跳到当前发的评论的位置,记得做类型转换
            redirect_url = article.get_absolute_url() + '#comment_elem_' + str(new_comment.id)

            # 当其参数是一个Model对象时，会自动调用这个Model对象的get_absolute_url()方法
            # return redirect(article)

            return redirect(redirect_url)
        else:
            return HttpResponse("表单内容有误，请重新填写")

    elif request.method == 'GET':
        comment_form = CommentForm()
        context = {}
        context['comment_form'] = comment_form
        context['article_id'] = article_id
        context['parent_comment_id'] = parent_comment_id
        return render(request, 'comment/reply.html', context)

    else:
        return HttpResponse("仅接受GET/POST请求")