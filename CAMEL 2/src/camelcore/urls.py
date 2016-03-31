from django.conf.urls import url

from .views.misc import IndexView

app_name = "camelcore"

urlpatterns = [
    url(r"^$", IndexView.as_view(), name="index"),
]
