from django.conf.urls import patterns, url

from core.views import (
    HomePageView, get_random_picture_params, login, like_picture
)


urlpatterns = patterns(
    '',
    url(r"^login/$", login, name="login"),
    url(
        r'^$',
        HomePageView.as_view(),
        name="homepage"
    ),
    url(
        r'^pictures/get-random-picture$',
        get_random_picture_params,
        name="random-picture"
    ),
    url(
        r'^pictures/like-picture/(?P<id>\d+)$',
        like_picture,
        name="like-picture"
    ),
)
