from django.conf.urls import include, url
from . import views

from module.views import ModuleIndexView, ModuleDashboardView, ModuleDetailsView

app_name = 'module'
urlpatterns = [
    url(r'^$', ModuleIndexView.as_view(), name='module_index'),
    url(r'^(?P<pk>\M\w+)/$', ModuleDetailsView.as_view(), name="module_detail"),
    url(r"^(?P<module_pk>\w+)/", include("latexbook.urls", namespace="latexbook")),
    url(r'^Dashboard/$', ModuleDashboardView.as_view(), name='module_dashboard'),
    url(r'^NewModule/$', views.new_module, name="new_module"),
]