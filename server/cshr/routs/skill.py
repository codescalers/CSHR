from django.urls import path

from server.cshr.views.skill import SkillsAPIView

urlpatterns = [
    path(
        "",
        SkillsAPIView.as_view({"get": "get_all", "post": "post"}),
        name="evaluation",
    ),
    path(
        "<str:id>/",
        SkillsAPIView.as_view(
            {"get": "get", "put": "put", "delete": "delete"}, name="evaluation-byId"
        ),
    ),
]
