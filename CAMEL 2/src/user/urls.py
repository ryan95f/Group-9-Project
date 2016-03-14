from django.conf.urls import url
from . import views

app_name = 'user'
urlpatterns = [
    url(r'login/', views.login_view, name='login'),
    url(r'^home/(?P<pk>\w+)/$', views.userhome, name="user_home"),
    url(r'^logout/$', views.logout_view, name="logout"),
]