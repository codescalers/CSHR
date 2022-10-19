from django.urls import path
from server.cshr.views.hr_letters import (
    HrLetterApiView,
    HrLetterUpdateApiView,
    BaseHrLetterApiView,
    HrLetterUserApiView,
    HrLetterAcceptApiView,
    HrLetterRejectApiView,
    GetAllUserDocumentsAPIView,
    BaseUserDocumentsAPIView,
)


urlpatterns = [
    path("", BaseHrLetterApiView.as_view()),
    path("user/", HrLetterUserApiView.as_view()),
    path("docs/", BaseUserDocumentsAPIView.as_view()),
    path("edit/<str:id>/", HrLetterUpdateApiView.as_view()),
    path("docs/<str:user_id>/", GetAllUserDocumentsAPIView.as_view()),
    path("accept/<str:id>/", HrLetterAcceptApiView.as_view()),
    path("reject/<str:id>/", HrLetterRejectApiView.as_view()),
    path("<str:id>/", HrLetterApiView.as_view()),
]
