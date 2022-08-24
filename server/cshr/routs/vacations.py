from django.urls import path
from server.cshr.views.vacations import Vacations_APIView, Vacations_Update_APIView


urlpatterns = [
    path("", Vacations_APIView.as_view({"get": "get_all", "post": "post"})),
    path(
        "<str:id>/", Vacations_APIView.as_view({"get": "get_one", "delete": "delete"})
    ),
    path(
        "edit/<str:id>/",
        Vacations_Update_APIView.as_view(
            {
                "put": "put",
            }
        ),
    ),
]
