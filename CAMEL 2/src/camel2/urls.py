"""camel2 URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r"^$", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r"^$", Home.as_view(), name="home")
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r"^blog/", include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    # Django Admin
    url(r"^admin/", admin.site.urls),

    # Project-specific
    url(r"^", include("camelcore.urls", namespace="camelcore")),

    # User app
    url(r"^user/", include("user.urls", namespace="user")),

    # Module app
    url(r"^module/", include("module.urls", namespace="module")),

    # Homework app
    url(r"^homework/", include("homeworkquiz.urls", namespace="homeworkquiz"))
]
