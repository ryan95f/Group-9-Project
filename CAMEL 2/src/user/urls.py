from django.conf.urls import url
from . import views
from user.views import UserView

app_name = 'user'
urlpatterns = [
    url(r'login/', views.login_view, name='login'),
    url(r'^home/(?P<pk>\w+)/$', views.userhome, name="user_home"),
    url(r'^logout/$', views.logout_view, name="logout"),
    url(r'^signup/$', UserView.as_view(), name="signup"),
]