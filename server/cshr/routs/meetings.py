from django.urls import path
from server.cshr.views.meetings import MeetingsApiView , BaseMeetingsApiView


urlpatterns = [
    path("", BaseMeetingsApiView.as_view()),
    path("<str:id>/", MeetingsApiView.as_view()),
]
