from django.urls import path


from server.cshr.views.users import (
    AdminUserAPIView,
    BaseAdminUserAPIView,
    GeneralUserAPIView,
    BaseGeneralUserAPIView,
    GetUsersInAdminOfficeAPIView,
    SetActiveUserAPIView,
    SetInActiveUserAPIView,
    TeamLeadUserAPIView,
    BaseTeamLeadUserAPIView,
    UserSkillsAPIView,
    TeamAPIView,
    TeamLeadsAPIView,
    PostUserSkillsAPIView,
    GetUsersBirthDatesAPIView,
)


urlpatterns = [
    path("", BaseGeneralUserAPIView.as_view()),
    path("set_inactive/", SetInActiveUserAPIView.as_view()),
    path("set_active/", SetActiveUserAPIView.as_view()),
    path("skills/", UserSkillsAPIView.as_view()),
    path("skills/add_skill/", PostUserSkillsAPIView.as_view()),
    path("team_lead/", BaseTeamLeadUserAPIView.as_view()),
    path("admin/", BaseAdminUserAPIView.as_view()),
    path("admin/office_users/", GetUsersInAdminOfficeAPIView.as_view()),
    path("team/", TeamAPIView.as_view()),
    path("birthdates/", GetUsersBirthDatesAPIView.as_view()),
    path("team/team_leads/", TeamLeadsAPIView.as_view()),
    path("team_lead/<str:id>/", TeamLeadUserAPIView.as_view()),
    path("admin/<str:id>/", AdminUserAPIView.as_view()),
    path("<str:id>/", GeneralUserAPIView.as_view()),
]
