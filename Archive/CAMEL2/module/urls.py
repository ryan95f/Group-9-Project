from django.conf.urls import url
from CAMEL2.settings import SITE_ROOT
from . import views
import os

app_name = 'module'
urlpatterns = [
    # list views
    url(r'^$', views.Module_ListView.as_view(), name='module_list'),
    url(r'^(?P<pk>\d+)$', views.Module_DetailView.as_view(), name="module_detail"),
    url(r'^book/(?P<pk>\d+)/$', views.Book_DetailView.as_view(), name="book_detail"),
    url(r'^chapter/(?P<pk>\d+)/$', views.Chapter_DetailView.as_view(), name="chapter_detail"),
    url(r'^booknode/(?P<pk>\d+)/$', views.BookNode_DetailView.as_view(), name="booknode_detail"),

    # selected node (by type)
    # eg homework
    url(r'^chapter/(?P<node_type>\w+)/(?P<pk>\d+)/$', views.selected, name="chapter_selected"),

    # image url
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(SITE_ROOT, 'media'),}, name="image_url"),
]