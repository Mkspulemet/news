from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
# from django.views.generic import ListView
from app_news.models import Article
from taggit.models import Tag
from app_news.forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from django.db.models import Count
from django.contrib.postgres.search import SearchVector
from mywebsite.settings import EMAIL_HOST_USER


# class ArticleListView(ListView):
#     queryset = Article.published.all()
#     context_object_name = 'articles'
#     paginate_by = 2
#     template_name = 'app_news/article/list.html'


def article_list(request, tag_slug=None):
    articles = Article.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        articles = articles.filter(tags__in=[tag])

    paginator = Paginator(articles, 2)
    page_number = request.GET.get('page', 1)
    try:
        articles = paginator.get_page(page_number)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        articles = paginator.page(1)
    return render(
        request,
        'app_news/article/list.html',
        {'articles': articles, 'tag': tag}
    )


def article_detail(request, year, month, day, article_slg):
    article = get_object_or_404(
        Article,
        status=Article.Status.PUBLISHED,
        slug=article_slg,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    comments = article.comments.filter(active=True)
    form = CommentForm()
    article_tags_ids = article.tags.values_list('id', flat=True)
    similar_articles = Article.published.filter(tags__in=article_tags_ids).exclude(
        id=article.id)
    similar_articles = similar_articles.annotate(same_tags=Count('tags')).order_by(
        '-same_tags', '-publish'
    )[:2]
    return render(
        request,
        'app_news/article/detail.html',
        {
            'article': article,
            'comments': comments,
            'form': form,
            'similar_articles': similar_articles
        }
    )


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
        request,
        'app_news/article/share.html',
        {'article': article, 'form': form, 'sent': sent},
    )


@require_POST
def article_comment(request, article_id):
    article = get_object_or_404(Article, id=article_id,
                                status=Article.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.article = article
        comment.save()
    return render(
        request,
        'app_news/article/comment.html',
        {'article': article, 'form': form, 'comment': comment},
    )


def article_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)

        if form.is_valid():
            query = form.cleaned_data['query']
            results = Article.published.annotate(
                search=SearchVector('headline', 'content')
            ).filter(search=query)
            print(results)

    return render(
        request,
        'app_news/article/search.html',
        {'form': form, 'query': query, 'results': results}
    )
