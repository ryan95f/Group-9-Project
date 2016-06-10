from django.conf.urls import url, include

from latexbook.views import BookNodeChapterDetailView, BookNodeDetailView, show_test

app_name = "latexbook"

urlpatterns = [
    url(r"^book/(?P<pk>[0-9]+)/$", BookNodeDetailView.as_view(), name="booknode_detail"),
    url(
        r"^book/(?P<book_pk>[0-9]+)/chapter/(?P<pk>[0-9]+)/$",
        BookNodeChapterDetailView.as_view(),
        name="booknode_chapter_detail"
    ),
    url(
        r"^book/(?P<book_pk>[0-9]+)/chapter/(?P<chapter_pk>[0-9]+)/",
        include("homeworkquiz.urls", namespace="homeworkquiz")
    ),
    url(r"test/$", show_test, name="test")
]
