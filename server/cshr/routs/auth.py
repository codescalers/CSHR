from django.urls import path
from server.cshr.views.auth import (
    RegisterApiView,
    LoginByTokenApiView,
    MyTokenRefreshView,
)


urlpatterns = [
    path("signup/", RegisterApiView.as_view()),
    path("login/", LoginByTokenApiView.as_view()),
    path("token/refresh/", MyTokenRefreshView.as_view()),
]
