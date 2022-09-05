from django.urls import path
from server.cshr.views.landing_page import LandingPageApiView


urlpatterns = [
    path(
        "",
        LandingPageApiView.as_view(),
    ),
]