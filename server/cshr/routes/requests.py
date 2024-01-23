"""this file will contain evertyting that related to requests model."""

from django.urls import path

from server.cshr.views.requests import RequestApiView

urlpatterns = [
    path("", RequestApiView.as_view()),
]
