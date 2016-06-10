from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.ReviewIndexView.as_view(), name="index"),

    url(r'^module/(?P<module_pk>\w+)/book/(?P<book_pk>[0-9]+)/question/(?P<question_pk>[0-9]+)/$',
        views.ReviewQuestionView.as_view(),
        name="question"
        ),

    url(r'^module/(?P<module_pk>\w+)/book/(?P<book_pk>[0-9]+)/$',
        views.ReviewBookView.as_view(),
        name="book_questions"
        ),

    url(r'^module/(?P<module_pk>\w+)/$', views.ReivewBookIndex.as_view(), name="book_index")
]
