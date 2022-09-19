from django.urls import path
from server.cshr.views.hr_letters import (
    HrLetterApiView,
    HrLetterUpdateApiView,
    BaseHrLetterApiView,
    HrLetterUserApiView,
)


urlpatterns = [
    path("", BaseHrLetterApiView.as_view()),
    path("user/", HrLetterUserApiView.as_view()),
    path("edit/<str:id>/", HrLetterUpdateApiView.as_view()),
    path("<str:id>/", HrLetterApiView.as_view()),
]
