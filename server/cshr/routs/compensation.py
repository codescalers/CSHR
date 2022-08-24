from django.urls import path
from server.cshr.views.compensation import CompensationAPIView

urlpatterns = [
    path("", CompensationAPIView.as_view({"post": "post", "get": "get_all"})),
    path(
        "<str:id>/",
        CompensationAPIView.as_view({"get": "get", "put": "put", "delete": "delete"}),
    ),
]
