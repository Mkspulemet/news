from django.urls import path
from .views import article_detail, ArticleListView, article_share

app_name = 'news'

urlpatterns = [
    # path('', article_list, name='article_list'),
    path('', ArticleListView.as_view(), name='article_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:article_slg>',
         article_detail, name='article_detail'),
    path('<int:article_id>/share', article_share,
         name='article_share'),
]
