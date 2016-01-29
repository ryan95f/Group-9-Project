from django.conf.urls import url
from . import views

app_name = 'homework'
urlpatterns = [
	#url(r'^(?P<pk>\d+)/$', views.homework, name="homework"),
    
    url(r'^(?P<pk>\d+)/$', views.Homework.as_view(), name="homework"),
    # edit_answers.html
    url(r'^answers/new/$', views.Edit_Answer.as_view(), name='new_answer',),
    url(r'^answers/edit/(?P<pk>\d+)/$', views.Edit_Answer.as_view(), name='edit_answer',),
    url(r'^answers/edit/(?P<pk>\d+)/ajax/$', views.Edit_Answer_Ajax.as_view(), name='edit_answer_ajax',),
    
    # multiple choice
    url(r'^sctest/(?P<pk>\d+)/$', views.sctest, name="sctest"),
]