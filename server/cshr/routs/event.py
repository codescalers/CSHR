from django.urls import path
from server.cshr.views.event import EventApiView, BaseEventsAPIView


urlpatterns = [
    path("", BaseEventsAPIView.as_view()),
    path(
        "<str:id>/",
        EventApiView.as_view({"get": "get_one", "delete": "delete", "put": "put"}),
    ),
]
