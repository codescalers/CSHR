from django.urls import path
from server.cshr.views.compensation import CompensationApiView

urlpatterns = [
    path("", CompensationApiView.as_view({"post": "post", "get": "get_all"})),
    path(
        "<str:id>/",
        CompensationApiView.as_view({"get": "get", "put": "put", "delete": "delete"}),
    ),
]
