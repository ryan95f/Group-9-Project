from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from user.views import UserView, LoginView, UserhomeView, LogoutView

app_name = 'user'
urlpatterns = [
    url(r'login/', LoginView.as_view(), name='login'),
    url(r'^home/(?P<pk>\w+)/$', login_required(UserhomeView.as_view()), name="user_home"),
    url(r'^logout/$', login_required(LogoutView.as_view()), name="logout"),
    url(r'^signup/$', UserView.as_view(), name="signup"),
]