from django.urls import path
from server.cshr.views.event import EventApiView, BaseEventsAPIView, GetEventOnDayAPIView


urlpatterns = [
    path("", BaseEventsAPIView.as_view()),
    path("exact/", GetEventOnDayAPIView.as_view()),
    path("<str:id>/", EventApiView.as_view()),
]
