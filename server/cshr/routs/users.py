from django.urls import path


from server.cshr.views.users import (
    AdminUserAPIView,
    GeneralUserAPIView,
    SupervisorUserAPIView,
    UserSkillsAPIView,
)


urlpatterns = [
    path("skills/", UserSkillsAPIView.as_view()),
    path("supervisor/<str:id>/", SupervisorUserAPIView.as_view({"get": "get_one"})),
    path("supervisor/", SupervisorUserAPIView.as_view({"get": "get_all"})),
    path(
        "admin/<str:id>/",
        AdminUserAPIView.as_view({"put": "put", "get": "get_one", "delete": "delete"}),
    ),
    path("admin/", AdminUserAPIView.as_view({"get": "get_all"})),
    path("", GeneralUserAPIView.as_view({"get": "get_all"})),
    path("<str:id>/", GeneralUserAPIView.as_view({"get": "get_one"})),
]
