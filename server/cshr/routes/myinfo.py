from django.urls import path

from ..views.users import SelfUserAPIView, UpdateUserProfileUserAPIView


urlpatterns = [
    path("", SelfUserAPIView.as_view()),
    path("update/profile/<str:id>/", UpdateUserProfileUserAPIView.as_view()),
]
