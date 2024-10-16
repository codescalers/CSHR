from django.urls import path
from cshr.views.compensation import CompensationApiView
from cshr.views.compensation import (
    CompensationUpdateApiView,
    BaseCompensationApiView,
    CompensationUserApiView,
    CompensationAcceptApiView,
    CompensationRejectApiView,
)

urlpatterns = [
    path("", BaseCompensationApiView.as_view()),
    path("user/", CompensationUserApiView.as_view()),
    path("edit/<str:id>/", CompensationUpdateApiView.as_view()),
    path("approve/<str:id>/", CompensationAcceptApiView.as_view()),
    path("reject/<str:id>/", CompensationRejectApiView.as_view()),
    path("<str:id>/", CompensationApiView.as_view()),
]
