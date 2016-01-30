from django.conf.urls import url
from . import views

app_name = 'module'
urlpatterns = [
    url(r'^$', views.module_index, name='module_index'),
    url(r'^(?P<pk>\w+)/$', views.module_detail, name="module_detail"),
]