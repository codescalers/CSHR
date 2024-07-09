"""this file will contain evertyting that related to notifications"""

from django.urls import path

from cshr.views.notifications import BaseNotificationApiView, ReadNotificationApiView, ReadAllNotificationsApiView, DeleteAllNotificationsApiView

urlpatterns = [
    path("", BaseNotificationApiView.as_view()),
    path("<str:notification_id>/", ReadNotificationApiView.as_view()),
    path("read-all/<str:user_id>/", ReadAllNotificationsApiView.as_view()),
    path("delete-all/<str:user_id>/", DeleteAllNotificationsApiView.as_view()),
]
