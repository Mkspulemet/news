from django.urls import path
from app_news.views import article_detail, article_share, article_comment, article_list


app_name = 'news'

urlpatterns = [
    # path('', ArticleListView.as_view(), name='article_list'),
    path('', article_list, name='article_list'),
    path('tag/<slug:tag_slug>/', article_list, name='article_list_by_tag'),
    path(
        '<int:year>/<int:month>/<int:day>/<slug:article_slg>/',
        article_detail,
        name='article_detail'
    ),
    path('<int:article_id>/share/', article_share, name='article_share'),
    path('<int:article_id>/comment/', article_comment, name='article_comment'),
]
