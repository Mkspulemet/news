from django.shortcuts import render, get_object_or_404

from .models import Article


def article_list(request):
    articles = Article.objects.all()
    return render(request, 'app_news/article/list.html', {'articles': articles})


def article_detail(request, id):
    article = get_object_or_404(Article, id=id)
    return render(request, 'app_news/article/detail.html', {'article': article})
