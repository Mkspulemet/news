from django.urls import path
from .views import article_list, article_detail

app_name = 'news'

urlpatterns = [
    path('', article_list, name='article_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:article_slg>', article_detail, name='article_detail'),
]
