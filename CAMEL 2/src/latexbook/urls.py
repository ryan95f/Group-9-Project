from django.conf.urls import url

from latexbook.views import book_create_view, BookNodeChapterDetailView, BookNodeDetailView, show_test

app_name = 'latexbook'
urlpatterns = [
    url(r"^create/book/$", book_create_view, name="bookcreate_form"),
    url(r"^book/(?P<pk>[0-9]+)/$", BookNodeDetailView.as_view(), name="booknode_detail"),
    url(
        r"^book/(?P<book_pk>[0-9]+)/chapter/(?P<pk>[0-9]+)/$",
        BookNodeChapterDetailView.as_view(),
        name="booknode_chapter_detail"
    ),
    url(r"test/$", show_test, name="test")
]
