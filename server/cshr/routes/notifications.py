"""this file will contain evertyting that related to notifications"""

from django.urls import path

from cshr.views.notifications import BaseNotificationApiView

urlpatterns = [
    path("", BaseNotificationApiView.as_view()),
]
