from django.urls import path


from server.cshr.views.users import (
    AdminUserAPIView,
    BaseAdminUserAPIView,
    GeneralUserAPIView,
    BaseGeneralUserAPIView,
    SupervisorUserAPIView,
    BaseSupervisorUserAPIView,
    UserSkillsAPIView,
    TeamAPIView,
    SupervisorsAPIView,
    PostUserSkillsAPIView,
    GetUsersBirthDatesAPIView,
)


urlpatterns = [
    path("skills/", UserSkillsAPIView.as_view()),
    path("skills/add_skill/", PostUserSkillsAPIView.as_view()),
    path("supervisor/", BaseSupervisorUserAPIView.as_view()),
    path("admin/", BaseAdminUserAPIView.as_view()),
    path("teams/", TeamAPIView.as_view()),
    path("birthdates/", GetUsersBirthDatesAPIView.as_view()),
    path("teams/supervisors/", SupervisorsAPIView.as_view()),
    path("supervisor/<str:id>/", SupervisorUserAPIView.as_view()),
    path("admin/<str:id>/", AdminUserAPIView.as_view()),
    path("", BaseGeneralUserAPIView.as_view()),
    path("<str:id>/", GeneralUserAPIView.as_view()),
]
