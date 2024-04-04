from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Article
from .forms import EmailPostForm
from django.core.mail import send_mail
from mywebsite.settings import EMAIL_HOST_USER


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


def article_share(request, article_id):
    sent = False
    article = get_object_or_404(Article, id=article_id,
                                status=Article.Status.PUBLISHED)
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            article_url = request.build_absolute_uri(article.get_absolute_url())

            subject = f'{cd["name"]} recommends you read {article.headline}'

            message = (
                f"Read {article.headline} at {article_url}\n\n"
                f"{cd['name']}'s comments: {cd['comment']}"
            )

            send_mail(subject, message, EMAIL_HOST_USER, [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(
        request, 'app_news/article/share.html',
        {'article': article, 'form': form, 'sent': sent}, )
