from django.shortcuts import render
from .base import BaseTemplateView


class SearchTemplateView(BaseTemplateView):
    template_name = 'index.html'
