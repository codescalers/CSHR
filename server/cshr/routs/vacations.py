from django.urls import path
from server.cshr.views.vacations import (
    VacationsUpdateApiView,
    BaseVacationsApiView,
    VacationsApiView,
    VacationUserApiView,
)


urlpatterns = [
    path("", BaseVacationsApiView.as_view()),
    path("user/", VacationUserApiView.as_view()),
    path("edit/<str:id>/", VacationsUpdateApiView.as_view()),
    path("<str:id>/", VacationsApiView.as_view()),
]
