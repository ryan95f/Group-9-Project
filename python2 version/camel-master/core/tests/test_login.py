from model_mommy import mommy
import pytest

from django.core.urlresolvers import reverse


def get_user_with_password(password):
    user = mommy.make("auth.User")
    user.set_password(password)
    user.save()
    return user

def test_not_logged_in_by_default(client):
    """
    Test that we're not logged in on accessing a page
    """
    response = client.get("/")
    assert response.context["user"].is_authenticated() is False

@pytest.mark.django_db
def test_successful_login_gets_logged_in_user(client):
    """
    Test that POSTing to login url with valid user/pw
    gets logged in user
    """
    user = get_user_with_password("FooBar")
    post_data = {"username": user.username, "password": "FooBar"}
    response = client.post(reverse("login"), post_data)
    assert response.context["user"].is_authenticated() is True
    assert response.context["user"] == user

@pytest.mark.django_db
def test_failed_login(client):
    """
    Test that a failed login (invalid user/pass combination) does
    not result in a logged in user
    """
    user = get_user_with_password("FooBar")
    post_data = {"username": user.username, "password": "NotRight"}
    response = client.post(reverse("login"), post_data)
    assert response.context["user"].is_authenticated() is False
