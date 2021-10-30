from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.ArticleListView.as_view()),
]
