from django.urls import path
from cshr.views.landing_page import LandingPageApiView


urlpatterns = [
    path(
        "",
        LandingPageApiView.as_view(),
    ),
]
