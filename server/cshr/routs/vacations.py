from django.urls import path
from server.cshr.views.vacations import VacationsUpdateApiView, BaseVacationsApiView , VacationsApiView


urlpatterns = [
    path("", BaseVacationsApiView.as_view()),
    path("edit/<str:id>/", VacationsUpdateApiView.as_view()),
    path("<str:id>/", VacationsApiView.as_view()),
    
]
