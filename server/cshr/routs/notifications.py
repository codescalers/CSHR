from django.urls import path
from server.cshr.views.notifications import NotificationApiView


urlpatterns = [
    path("", NotificationApiView.as_view({"get": "get_all", "post": "post"})),
    path(
        "<str:id>/",
        NotificationApiView.as_view(
            {"get": "get_one", "delete": "delete", "put": "put"}
        ),
    ),
]
