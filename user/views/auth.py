from django.contrib.auth import views
from django.shortcuts import render
from django.urls import reverse_lazy

from ..forms import UserForm
from .base import (
    BaseTemplateView,
    BaseCreateView,
)


class LoginTemplateView(views.LoginView):
    template_name = 'auth/login.html'

    def get_success_url(self):
        return reverse_lazy('user:index')


class RegisterTemplateView(BaseCreateView):
    template_name = 'auth/register.html'
    success_url = reverse_lazy('user:auth.login')
    form_class = UserForm


class LogoutView(views.LogoutView):
    next_page = reverse_lazy('user:index')
