from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required

from module.views import ModuleIndexView, ModuleDashboardView, ModuleDetailsView, NewModule

app_name = 'module'
urlpatterns = [
    url(r'^$', ModuleIndexView.as_view(), name='module_index'),
    url(r'^(?P<pk>\M\w+)/$', ModuleDetailsView.as_view(), name="module_detail"),
    url(r"^(?P<module_pk>\w+)/", include("latexbook.urls", namespace="latexbook")),
    url(r'^Dashboard/$', login_required(ModuleDashboardView.as_view()), name='module_dashboard'),
    url(r'^NewModule/$', NewModule.as_view(), name="new_module"),
]
