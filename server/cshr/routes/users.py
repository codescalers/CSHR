from django.urls import path


from cshr.views.users import (
    AdminUserAPIView,
    BaseAdminUserAPIView,
    GeneralUserAPIView,
    BaseGeneralUserAPIView,
    GetUsersInAdminOfficeAPIView,
    SetActiveUserAPIView,
    SetInActiveUserAPIView,
    SupervisorUserAPIView,
    BaseSupervisorUserAPIView,
    UserSkillsAPIView,
    TeamAPIView,
    TeamSupervisorsAPIView,
    SupervisorsAPIView,
    PostUserSkillsAPIView,
    GetUsersBirthDatesAPIView,
)


urlpatterns = [
    path("", BaseGeneralUserAPIView.as_view()),
    path("set_inactive/", SetInActiveUserAPIView.as_view()),
    path("set_active/", SetActiveUserAPIView.as_view()),
    path("skills/", UserSkillsAPIView.as_view()),
    path("skills/add_skill/", PostUserSkillsAPIView.as_view()),
    path("supervisor/", BaseSupervisorUserAPIView.as_view()),
    path("admin/", BaseAdminUserAPIView.as_view()),
    path("admin/office_users/", GetUsersInAdminOfficeAPIView.as_view()),
    path("team/", TeamAPIView.as_view()),
    path("birthdates/", GetUsersBirthDatesAPIView.as_view()),
    path("team/supervisors/", TeamSupervisorsAPIView.as_view()),
    path("supervisors/", SupervisorsAPIView.as_view()),
    path("supervisor/<str:id>/", SupervisorUserAPIView.as_view()),
    path("admin/<str:id>/", AdminUserAPIView.as_view()),
    path("<str:id>/", GeneralUserAPIView.as_view()),
]
