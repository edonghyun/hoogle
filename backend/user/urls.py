from django.urls import path, include
from django.views.generic import TemplateView

from . import views

app_name = 'user'

urlpatterns = [
    path('', views.SearchListView.as_view(), name='index'),
    path('auth/login/', views.LoginTemplateView.as_view(), name='auth.login'),
    path('auth/logout/', views.LogoutView.as_view(), name='auth.logout'),
    path('auth/register/', views.RegisterTemplateView.as_view(), name='auth.register'),
]
