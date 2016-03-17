from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    """Displays index (home) page of CAMEL"""
    template_name = 'camelcore/index.html'
