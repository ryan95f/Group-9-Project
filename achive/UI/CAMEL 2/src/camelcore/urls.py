from django.conf.urls import include, url

from .views import IndexView

app_name = "camelcore"

urlpatterns = [
    url(r"^$", IndexView.as_view(), name="index"),
    url(r"^moduledashboard/", include("camelcore.moduledashboard.urls", namespace="module_dashboard"))
]
