from django.conf.urls import url

from .views import book_add_detail_view, book_add_view, book_create_view, book_delete_view

app_name = "camelcore"

urlpatterns = [
    url(r"^(?P<module_pk>\w+)/add/book/$", book_add_detail_view, name="add_detail_book"),
    url(r"^(?P<module_pk>\w+)/add/book/(?P<book_pk>\w+)/$", book_add_view, name="add_book"),
    url(r"^(?P<module_pk>\w+)/create/book/$", book_create_view, name="create_book"),
    url(r"^(?P<module_pk>\w+)/delete/book/(?P<book_pk>\w+)/$", book_delete_view, name="delete_book"),
]
