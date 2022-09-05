from django.urls import path
from server.cshr.views.hr_letters import HrLetterApiView, HrLetterUpdateApiView


urlpatterns = [
    path("", HrLetterApiView.as_view({"get": "get_all", "post": "post"})),
    path("<str:id>/", HrLetterApiView.as_view({"get": "get_one", "delete": "delete"})),
    path(
        "edit/<str:id>/",
        HrLetterUpdateApiView.as_view(
            {
                "put": "put",
            }
        ),
    ),
]