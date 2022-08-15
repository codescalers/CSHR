from django.urls import path
from server.cshr.views.auth import *


urlpatterns = [
    path('signup/', RegisterAPIView.as_view()),
    path('login/', LoginByTokenAPIView.as_view()),
    path('token/refresh/', MyTokenRefreshView.as_view()),
    path('settings/', UpdateUserSettingsAPIView.as_view()),
]