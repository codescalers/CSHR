from django.urls import path
from server.cshr.views.event import EventApiView


urlpatterns = [
    path("", EventApiView.as_view({"get": "get_all", "post": "post"})),
    path(
        "<str:id>/",
        EventApiView.as_view({"get": "get_one", "delete": "delete", "put": "put"}),
    ),
]
