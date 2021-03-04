from django.shortcuts import render
from core.models import Article
from .base import BaseListView


class SearchListView(BaseListView):
    model = Article
    template_name = 'index.html'

    def get_queryset(self):
        query = self.request.GET.get('query')
        if not query:
            return []

        queryset = super().get_queryset()
        return queryset
