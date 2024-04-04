from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Article


class ArticleListView(ListView):
    queryset = Article.published.all()
    context_object_name = 'articles'
    paginate_by = 2
    template_name = 'app_news/article/list.html'


# def article_list(request):
#     articles = Article.published.all()
#     paginator = Paginator(articles, 2)
#     page_number = request.GET.get('page', 1)
#     try:
#         articles = paginator.get_page(page_number)
#     except EmptyPage:
#         articles = paginator.page(paginator.num_pages)
#     except PageNotAnInteger:
#         articles = paginator.page(1)
#     return render(request, 'app_news/article/list.html', {'articles': articles})


def article_detail(request, year, month, day, article_slg):
    article = get_object_or_404(
        Article,
        status=Article.Status.PUBLISHED,
        slug=article_slg,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    return render(request, 'app_news/article/detail.html', {'article': article})
