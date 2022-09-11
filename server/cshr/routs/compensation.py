from django.urls import path
from server.cshr.views.compensation import CompensationApiView
from server.cshr.views.compensation import CompensationUpdateApiView

urlpatterns = [
    path("", CompensationApiView.as_view({"post": "post", "get": "get_all"})),
    path(
        "<str:id>/",
        CompensationApiView.as_view({"get": "get", "delete": "delete"}),
    ),
    path(
        "edit/<str:id>/",
        CompensationUpdateApiView.as_view(
            {
                "put": "put",
            }
        ),
    ),
]
