from django.conf.urls import include, url
from homework.views import HomeworkView

app_name = 'homework'
urlpatterns = [
	 url(r'^test/$', HomeworkView.as_view(), name='homework'),
]