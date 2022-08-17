from django.urls import path
from server.cshr.views.user import (
    UserAPIView,
    UsersAPIView
)


urlpatterns = [
    path("/user/", UserAPIView.as_view(), name="user"),
    path("/users/", UsersAPIView.as_view(), name="users")
]
