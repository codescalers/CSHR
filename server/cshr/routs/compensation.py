from django.urls import path
from server.cshr.views.compensation import CompensationApiView
from server.cshr.views.compensation import (
    CompensationUpdateApiView,
    BaseCompensationApiView,
    CompensationUserApiView,
)

urlpatterns = [
    path("", BaseCompensationApiView.as_view()),
    path("user/", CompensationUserApiView.as_view()),
    path("edit/<str:id>/", CompensationUpdateApiView.as_view()),
    path("<str:id>/", CompensationApiView.as_view()),
]
