from django.urls import path
from app_news.views import article_detail, ArticleListView, article_share, article_comment

app_name = 'news'

urlpatterns = [
    path('', ArticleListView.as_view(), name='article_list'),
    path(
        '<int:year>/<int:month>/<int:day>/<slug:article_slg>/',
        article_detail,
        name='article_detail'
    ),
    path(
        '<int:article_id>/share/',
        article_share,
        name='article_share'
    ),
    path(
        '<int:article_id>/comment',
        article_comment,
        name='article_comment'
    ),
]
