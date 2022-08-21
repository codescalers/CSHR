from django.urls import path
from server.cshr.views.users import UserAPIView


urlpatterns = [
    path("user/<str:id>", UserAPIView.as_view({
        'get': 'get_one',
        'delete': 'delete',
        'put': 'put'
    }), name="user"),
    path("user/", UserAPIView.as_view({
        'post': 'post',
    }), name="users_post"), 
    path("user/search/<str:search_input>", UserAPIView.as_view({
        'get': 'search_input',
    }), name="users_post"),
    path("users/", UserAPIView.as_view({
        'get': 'get_all'
    }), name="users_get")
]
