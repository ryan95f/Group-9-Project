from django.conf.urls import url
from homeworkquiz.views import save_answer, SingleChoiceSaveView, JaxSaveView, QuestionDetailView

app_name = 'homeworkquiz'
urlpatterns = [
    # urls fors saving / submitting each question type
    url(r'^save-jax/(?P<node_pk>\d+)/$', JaxSaveView.as_view(), name="jaxquestion"),
    url(r'^save-multi/(?P<node_pk>\d+)/$', save_answer, name="multiquestion"),
    url(r'^save-single/(?P<node_pk>\d+)/$', SingleChoiceSaveView.as_view(), name="singlequestion"),
    url(r'^question/(?P<pk>\d+)/$', QuestionDetailView.as_view(), name="do_question")
]
