from django.conf.urls import url

from latexbook.views import show_test

urlpatterns = [
    url(r"test/$", show_test, name="latexbook_booknode_detail")
]
