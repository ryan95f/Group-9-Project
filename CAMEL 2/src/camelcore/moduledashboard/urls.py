from django.conf.urls import url

from .views import book_create_view, book_delete_view

app_name = "camelcore"

urlpatterns = [
    url(r"^(?P<module_pk>\w+)/create/book/$", book_create_view, name="create_book"),
    url(r"^(?P<module_pk>\w+)/add/book/$", book_create_view, name="add_book"),
    url(r"^(?P<module_pk>\w+)/delete/book/(?P<book_pk>\w+)/$", book_delete_view, name="delete_book"),
]
