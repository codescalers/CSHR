from django.urls import path
from server.cshr.views.hr_letters import (
    HrLetterApiView,
    HrLetterUpdateApiView,
    BaseHrLetterApiView,
    HrLetterUserApiView,
    HrLetterAcceptApiView,
    HrLetterRejectApiView,
)


urlpatterns = [
    path("", BaseHrLetterApiView.as_view()),
    path("user/", HrLetterUserApiView.as_view()),
    path("edit/<str:id>/", HrLetterUpdateApiView.as_view()),
    path("accept/<str:id>/", HrLetterAcceptApiView.as_view()),
    path("reject/<str:id>/", HrLetterRejectApiView.as_view()),
    path("<str:id>/", HrLetterApiView.as_view()),
]
