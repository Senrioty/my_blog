import markdown
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Q
from django.views.generic import ListView,DetailView
from .models import Article,ArticleColumn
from .form import ArticleForm


# 类视图
class ArticleListView(ListView):
    # 上下文的名称
    context_object_name = 'article'
    # 查询集
    queryset = Article.objects.all()
    # 模板位置
    template_name = 'article/list.html'

    # def get_queryset(self):
    #     queryset = Article.objects.filter(title='Python')
    #     return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        # 获取原有的上下文
        context = super().get_context_data(**kwargs)
        # 增加新上下文
        context['order'] = 'total_views'
        return context


class ArticleDetailView(DetailView):
    queryset = Article.objects.all()
    context_object_name = 'article'
    template_name = 'article/detail.html'


# Create your views here.
def article_list(request):

    search = request.GET.get('search')
    order = request.GET.get('order')

    if search:

        # 根据GET请求中的查询条件，返回不同的排序对象
        if order == 'total_views':
            # articles = Article.objects.all().order_by('-total_views')
            articles = Article.objects.filter(
                Q(title__icontains=search)  |
                Q(content__icontains=search)
            ).order_by('-total_views')
        else:
            articles = Article.objects.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search)
            )

    else:
        # 将search置空,因为用户没有搜索，则search=None,相当于模板中查的是“None”的字符串
        search = ''
        if order == 'total_views':
            articles = Article.objects.all().order_by('-total_views')
        else:
            articles = Article.objects.all()

    paginator = Paginator(articles, settings.ARTICLE_OF_PAGE)
    page = request.GET.get('page', 1)
    page_of_articles = paginator.get_page(page)

    context = {}
    context['page_of_articles'] = page_of_articles
    context['order'] = order  # 提供给翻页
    context['search'] = search
    return render(request, 'article/list.html', context)


def article_detail(request, id):
    article = Article.objects.get(id=id)

    # 处理阅读量
    article.total_views += 1
    article.save(update_fields=['total_views'])  # 指定只更新total_views字段，优化执行效率

    # 将markdown语法渲染成html样式
    md = markdown.Markdown(
        extensions=[
            # 包含 缩写、表格等常用扩展
            'markdown.extensions.extra',
            # 语法高亮扩展
            'markdown.extensions.codehilite',
            # 目录扩展
            'markdown.extensions.toc',
        ])

    article.content = md.convert(article.content)

    context = {}
    context['article'] = article
    context['toc'] = md.toc
    return render(request, 'article/detail.html', context)


def article_create(request):
    if request.method == 'POST':
        article_form = ArticleForm(request.POST)
        if article_form.is_valid():
            new_article = article_form.save(commit=False)
            new_article.author = User.objects.get(id=request.user.id)

            # 保存栏目
            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id=request.POST.get('column'))

            new_article.save()
            return redirect("article:article_list")
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        article_form = ArticleForm()
        context = {}
        context['article_form'] = article_form
        context['columns'] = ArticleColumn.objects.all()
        return render(request, 'article/create.html', context)


def article_delete(request, id):
    article = Article.objects.get(id=id)
    article.delete()
    return redirect('article:article_list')


def article_safe_delete(request, id):
    if request.method == 'POST':
        article = Article.objects.get(id=id)
        article.delete()
        return redirect('article:article_list')
    else:
        return HttpResponse("仅允许post请求")


def article_update(request, id):
    article = Article.objects.get(id=id)

    # 前端不可信原则，后端要再次过滤非作者的用户
    if request.user != article.author:
        return HttpResponse("抱歉，你无权修改这篇文章")

    if request.method == "POST":
        article_form = ArticleForm(request.POST)
        if article_form.is_valid():
            article.title = article_form.cleaned_data['title']
            article.content = article_form.cleaned_data['content']

            # 处理栏目
            if request.POST['column'] != 'none':
                article.column = ArticleColumn.objects.get(id=request.POST['column'])
            else:
                article.column = None

            article.save()
            return redirect('article:article_detail', id=id)
        else:
            return HttpResponse("表单内容有误，请重新填写")
    else:
        article_form = ArticleForm()
        context = {}
        context['article'] = article
        context['article_form'] = article_form
        context['columns'] = ArticleColumn.objects.all()
        return render(request, 'article/update.html', context)