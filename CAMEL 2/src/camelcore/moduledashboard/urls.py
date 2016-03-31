from django.conf.urls import url

from .views import book_create_view

app_name = "camelcore"

urlpatterns = [
    url(r"^(?P<module_pk>\w+)/create/book/$", book_create_view, name="create_book"),
]
