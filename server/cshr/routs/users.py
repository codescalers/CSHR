from django.urls import path
from server.cshr.views.users import (
    UserAPIView,
    UsersAPIView
)


urlpatterns = [
    path("user/<str:id>", UserAPIView.as_view({
        'get': 'get_one',
        'delete': 'delete',
        'put': 'put'
    }), name="user"),
    path("user/", UsersAPIView.as_view({
        'post': 'post',

    }), name="users"),
    path("users/", UsersAPIView.as_view({
        'get': 'get_all'
    }), name="users")
]
