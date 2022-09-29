"""this file will contain evertyting that related to notifications"""

from django.urls import path

from server.cshr.views.notifications import BaseNotificationApiView

urlpatterns = [
    path("", BaseNotificationApiView.as_view()),
]
