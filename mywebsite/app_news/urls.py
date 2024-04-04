from django.urls import path
from .views import article_detail, ArticleListView


app_name = 'news'

urlpatterns = [
    # path('', article_list, name='article_list'),
    path('', ArticleListView.as_view(), name='article_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:article_slg>',
         article_detail, name='article_detail'),
]
