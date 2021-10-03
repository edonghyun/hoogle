from django.views.generic import (
    TemplateView,
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)

from .mixin import BaseViewMixin


class BaseTemplateView(BaseViewMixin, TemplateView):
    pass


class BaseCreateView(BaseViewMixin, CreateView):
    pass


class BaseListView(BaseViewMixin, ListView):
    pass


class BaseDetailView(BaseViewMixin, DetailView):
    pass


class BaseUpdateView(BaseViewMixin, UpdateView):
    pass


class BaseDeleteView(BaseViewMixin, DeleteView):
    pass
