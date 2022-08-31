from django.urls import path
from server.cshr.views.meetings import MeetingsApiView


urlpatterns = [
    path("", MeetingsApiView.as_view({"get": "get_all", "post": "post"})),
    path(
        "<str:id>/",
        MeetingsApiView.as_view({"get": "get_one", "delete": "delete", "put": "put"}),
    ),
]
