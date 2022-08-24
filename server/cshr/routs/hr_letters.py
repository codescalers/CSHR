from django.urls import path
from server.cshr.views.hr_letters import HR_Letter_APIView, HR_Letter_Update_APIView


urlpatterns = [
    path("", HR_Letter_APIView.as_view({"get": "get_all", "post": "post"})),
    path(
        "<str:id>/", HR_Letter_APIView.as_view({"get": "get_one", "delete": "delete"})
    ),
    path(
        "edit/<str:id>/",
        HR_Letter_Update_APIView.as_view(
            {
                "put": "put",
            }
        ),
    ),
]
