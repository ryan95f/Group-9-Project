from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from homeworkquiz.views import save_answer, SingleChoiceSaveView, JaxSaveView, QuestionDetailView

app_name = 'homeworkquiz'
urlpatterns = [
    # urls fors saving / submitting each question type
    url(r'^save-jax/(?P<node_pk>\d+)/$', JaxSaveView.as_view(), name="jaxquestion"),
    url(r'^save-multi/(?P<node_pk>\d+)/$', save_answer, name="multiquestion"),
    url(r'^save-single/(?P<node_pk>\d+)/$', SingleChoiceSaveView.as_view(), name="singlequestion"),

    # url for question answering page
    url(r'^question/(?P<pk>\d+)/$', login_required(QuestionDetailView.as_view()), name="do_question")
]
