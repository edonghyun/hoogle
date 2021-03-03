from django.contrib.auth import views
from django.shortcuts import render
from django.urls import reverse_lazy

from .base import BaseTemplateView


class LoginTemplateView(views.LoginView):
    template_name = 'auth/login.html'
    success_url = 'index.html'


class LogoutView(views.LogoutView):
    next_page = reverse_lazy('index')


class RegisterTemplateView(BaseTemplateView):
    next_page = reverse_lazy('auth/register.html')
