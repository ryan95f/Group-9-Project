from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import book_add_detail_view, book_add_view, book_create_view, book_delete_view

app_name = "camelcore"

urlpatterns = [
    url(r"^(?P<module_pk>\w+)/add/book/$", login_required(book_add_detail_view), name="add_detail_book"),
    url(r"^(?P<module_pk>\w+)/add/book/(?P<book_pk>\w+)/$", login_required(book_add_view), name="add_book"),
    url(r"^(?P<module_pk>\w+)/create/book/$", login_required(book_create_view), name="create_book"),
    url(r"^(?P<module_pk>\w+)/delete/book/(?P<book_pk>\w+)/$", login_required(book_delete_view), name="delete_book"),
]
